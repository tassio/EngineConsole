#-*- coding: utf-8 -*-

from engineConsole.base.telaConsole import TelaConsole
from engineConsole.painelConsole import PainelConsole
from engineConsole.labelConsole import LabelConsole
from engineConsole.base.engine import EngineConsole


class StackedWidgetConsole(PainelConsole):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._visivel = 0

    def indVisivel(self):
        return self._visivel if self.numTelas()!=0 else -1

    def addTela(self, tela):
        super().addTela(tela)
        self._atualizaVisiveis()

    def removeTela(self, tela):
        super().removeTela(tela)
        ind = self.indVisivel()
        if ind != -1:
            self._visivel = min(self._visivel, self.numTelas()-1)

        self._atualizaVisiveis()

    def removeTelasNaoVisiveis(self):
        telaVisivel = self.getTelaVisivel()
        if telaVisivel:
            self.removeTelas()
            self.addTela(telaVisivel)
            self._visivel = 0
            self._atualizaVisiveis()

    def setVisivel(self, ind):
        if 0 <= ind < self.numTelas():
            self._visivel = ind
            self._atualizaVisiveis()

    def focusNextChild(self):
        """Passa o foco para o proximo filho"""
        tela = self.getTelaVisivel()
        return tela and tela.focusNextChild()

    def focusPreviousChild(self):
        """Passa o foco para o filho anterior"""
        tela = self.getTelaVisivel()
        return tela and tela.focusPreviousChild()

    def indexChildActive(self):
        """Retorna o indice do filho ativo"""
        tela = self.getTelaVisivel()
        if tela and tela.activeWindow():
            return self.indVisivel()

        return -1

    def getTelaVisivel(self):
        ind = self.indVisivel()
        if ind != -1:
            return self.getChilds()[ind]

    def _atualizaVisiveis(self):
        """Mostra a tela selecionada e esconde todas as outras"""
        for i in range(self.numTelas()):
            if i == self.indVisivel():
                if not self.getChilds()[i].isVisible():
                    self.getChilds()[i].setVisible(True)

            elif self.getChilds()[i].isVisible():
                self.getChilds()[i].setVisible(False)

        self.update()

    def acceptFocus(self):
        return False

    def desenhoTela(self, tam):
        return self.getTelaVisivel().desenhoTelaConsole(tam)


class TabTelaConsole(TelaConsole):
    MAX_TITULOS = 9
    def __init__(self, parent=None):
        super().__init__(parent)
        self._layout = StackedWidgetConsole(self)
        self._titulos = []

    def focusNextChild(self):
        if self.numTitulos() == 0:
            return False

        if self._layout.indexChildActive() == -1 and self.isVisible() and not self.hasFocus() and self.acceptFocus():
            self.setFocus()
            return True

        return self._layout.focusNextChild()

    def focusPreviousChild(self):
        if self.numTitulos() == 0:
            return False

        if self._layout.indexChildActive() != -1 and self.isVisible() and not self.hasFocus() and self.acceptFocus():
            self.setFocus()
            return True

        return self._layout.focusPreviousChild()

    def temSelecionado(self):
        """Verifica se tem alguma aba selecionada"""
        return self._layout.indVisivel() != -1

    def setSelecionado(self, sel):
        """Modifica o selecionado para o indice passado, se ele existe na lista"""
        if 0 <= sel < self._layout.numTelas():
            self._layout.setVisivel(sel)

    def getSelecionado(self):
        return self._layout.indVisivel()

    def telaVisivel(self):
        """Retorna a tela visivel no momento"""
        return self._layout.getTelaVisivel()

    def tituloSelecionado(self):
        """Retorna o titulo selecionado no momento"""
        return self._titulos[self._layout.indVisivel()] if self._layout.indVisivel() != -1 else None

    def numTitulos(self):
        return len(self._titulos)

    def modificarTitulo(self, ind, titulo):
        if 0 <= ind < self.numTitulos():
            self._titulos[ind] = LabelConsole(titulo, LabelConsole.CENTER)
            self.update()

    def addTela(self, titulo, tela):
        """Adiciona uma tela na tabTela"""
        if isinstance(titulo, str):
            if len(self._titulos) < TabTelaConsole.MAX_TITULOS:
                self._titulos.append(LabelConsole(titulo, LabelConsole.CENTER))
                self._layout.addTela(tela)
                self.update()
        else:
            raise TypeError("Titulo deve ser uma string")

    def removeTela(self, titulo_or_tela):
        ind = -1
        if isinstance(titulo_or_tela, str):
            if titulo_or_tela in self._titulos:
                ind = self._titulos.index(titulo_or_tela)
        else:
            if titulo_or_tela in self._layout.getChilds():
                ind = self._layout.getChilds().index(titulo_or_tela)

        if ind != -1:
            self._titulos.pop(ind)
            self._layout.removeTela(titulo_or_tela)
            self.update()

    def removeTelaVisivel(self):
        tela = self.telaVisivel()
        if tela:
            self.removeTela(tela)

    def removeTelasNaoVisiveis(self):
        if self.temSelecionado():
            self._titulos = [self.tituloSelecionado()]
            self._layout.removeTelasNaoVisiveis()
            self.update()

    def acceptFocus(self):
        return True

    def onDirecional(self, direc):
        if direc in [EngineConsole.UP, EngineConsole.LEFT]:
            self.setSelecionado(self.getSelecionado() - 1)
        else:
            self.setSelecionado(self.getSelecionado() + 1)

    def desenhoTela(self, tam):
        if len(self._titulos) == 0:
            s = '|{0:->{1}}|\n'.format('', tam-2)
            s += '|{0:<{1}}|\n'.format(LabelConsole("VAZIO", LabelConsole.CENTER).desenhoTelaConsole(tam-2), tam-2)
            s += '|{0:-<{1}}|'.format('', tam-2)
            return s


        tamBarra = int((tam - len(self._titulos)+1) / len(self._titulos))

        s = ' '.join(['|{0:-<{1}}|'.format('', tamBarra-2)]*len(self._titulos)) + '\n'
        s += ' '.join(['|{2}{0:<{1}}{2}|'.format(i.desenhoTelaConsole(tamBarra-4), tamBarra-4, [' ','+'][self.tituloSelecionado() == i]) for i in self._titulos]) + '\n'
        s += '|{0:-<{1}}|\n'.format('', tam-2)

        for linha in self._layout.getTelaVisivel().desenhoTelaConsole(tam-2).split('\n'):
            s += '|{0:<{1}}|\n'.format(linha, tam-2)

        s += '|{0:->{1}}|'.format(['-', '*'][self.hasFocus()], tam-2)
        return s

    
