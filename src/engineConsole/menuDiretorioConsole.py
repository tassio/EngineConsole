#-*- coding: utf-8 -*-

from PyQt4.QtCore import pyqtSignal, QDir, QFileInfo

from engineConsole.painelConsole import PainelConsole
from engineConsole.listaConsole import MatrizConsole
from engineConsole.labelConsole import LabelConsole
from engineConsole.editConsole import LabelEditConsole
from engineConsole.buttonConsole import PainelBotoesConsole


class MenuDiretorioConsole(MatrizConsole):
    arquivoSelecionado = pyqtSignal(str)
    def __init__(self, initDir='.', parent=None):
        super().__init__(parent=parent)

        self._dir = QDir(initDir)
        self._dir.setSorting(QDir.Name)
        self._addItensDir()

    def _addItensDir(self):
        self.clear()
        di = self._dir.entryList()
        try:
            di.remove('.')
        except ValueError:
            pass

        self.addItens([LabelConsole(i) for i in di])

    def atualizarListaArquivos(self):
        self.cd('.')

    def cd(self, diret):
        if self._dir.cd(diret):
            self._addItensDir()
            return True

        return False

    def onEnter(self):
        if not self.cd(self.getItemSelecionado().getTexto()):
            self.arquivoSelecionado.emit(self.pathArquivoSelecionado())

    def path(self):
        return self._dir.absolutePath()

    def pathArquivoSelecionado(self):
        return self.path() + '/' + self.getItemSelecionado().getTexto()

    def desenhoTela(self, tam):
        s = '|{0:-<{1}}|\n'.format('',tam-2)
        s += '|Path: {0:<{1}}{2}|\n'.format(LabelConsole(self._dir.absolutePath()).desenhoTelaConsole(tam-9), tam-9, [' ','*'][self.hasFocus()])
        s += '|{0:-<{1}}|\n'.format('',tam-2)
        for i in super().desenhoTela(tam-2).split('\n'):
            s += '|{0:<{1}}|\n'.format(i, tam-2)
        s += '|{0:-<{1}}|'.format('',tam-2)

        return s


class PainelDiretorioConsole(PainelConsole):
    arquivoSelecionado = pyqtSignal(str)
    def __init__(self, initDir='.', parent=None):
        super().__init__(parent)
        self._menu = MenuDiretorioConsole(initDir)
        self._edit = LabelEditConsole("Nome")
        painelButton = PainelBotoesConsole()
        self._btnAceitar = painelButton.addButton("Aceitar")

        self.addTela(self._menu)
        self.addTela(self._edit)
        self.addTela(painelButton)

        self._menu.selecaoModificada.connect(self._mudarTextoEdit)

    def _mudarTextoEdit(self, texto):
        if texto != '..':
            self._edit.setTexto(texto)

    def desenhoTela(self, tam):
        s = '|{0:-<{1}}|\n'.format('',tam-2)
        for i in super().desenhoTela(tam-2).split('\n'):
            s += '|{0:{1}}|\n'.format(i, tam-2)
        s += '|{0:-<{1}}|'.format('',tam-2)

        return s


class MenuAbrirArquivoConsole(PainelDiretorioConsole):
    def __init__(self, initDir='.', parent=None):
        super().__init__(initDir, parent)
        self._btnAceitar.setTexto("Abrir")
        self._btnAceitar.enterPressed.connect(self._abrir)
        self._menu.arquivoSelecionado.connect(self._abrirArquivo)
        self._edit.setVisible(False)

    def _abrir(self):
        path = self._menu.pathArquivoSelecionado()
        if QFileInfo(path).isDir():
            self._menu.cd(path)
        else:
            self._abrirArquivo(path)

    def _abrirArquivo(self, arq):
        if QFileInfo(arq).isFile():
            self.arquivoSelecionado.emit(arq)


class MenuSalvarArquivoConsole(PainelDiretorioConsole):
    def __init__(self, initDir='.', parent=None):
        super().__init__(initDir, parent)
        self._configurarPainel()
        self._menu.arquivoSelecionado.connect(lambda arq: self._salvar())
        self._btnAceitar.setTexto("Salvar")
        self._btnAceitar.enterPressed.connect(self._salvar)
        self._edit.enterPressed.connect(self._salvar)

    def _configurarPainel(self):
        self._painelSobrescrever = PainelConsole()

        self._lblArquivoSobrescrever = LabelConsole()
        self._lblSobrescrever = LabelConsole("Voce deseja sobrescrever esse arquivo?")
        self._painelBtn = PainelBotoesConsole()
        self._btnSobrescreverSim = self._painelBtn.addButton("Sim")
        self._btnSobrescreverSim.enterPressed.connect(lambda: self._salvarArquivo(self._lblArquivoSobrescrever.getTexto()))
        self._btnSobrescreverNao = self._painelBtn.addButton("Nao")
        self._btnSobrescreverNao.enterPressed.connect(lambda: self._telaSobrescrever(False))

        self._painelSobrescrever.addTela(self._lblArquivoSobrescrever)
        self._painelSobrescrever.addTela(self._lblSobrescrever)
        self._painelSobrescrever.addTela(self._painelBtn)
        self._painelSobrescrever.setVisible(False)

        self.addTela(self._painelSobrescrever)

    def _telaSobrescrever(self, mostrar):
        for i in [self._btnAceitar, self._edit, self._menu]:
            i.setVisible(not mostrar)

        self._painelSobrescrever.setVisible(mostrar)

        if not mostrar:
            self._menu.setFocus()
        else:
            self._btnSobrescreverSim.setFocus()

    def _salvar(self):
        path = self._menu.path() + '/' + self._edit.getTexto()
        if QFileInfo(path).exists():
            self._lblArquivoSobrescrever.setTexto(path)
            self._telaSobrescrever(True)
        else:
            self._salvarArquivo(path)

    def _salvarArquivo(self, arq):
        self.arquivoSelecionado.emit(arq)
        if not self._menu.isVisible():
            self._telaSobrescrever(False)


