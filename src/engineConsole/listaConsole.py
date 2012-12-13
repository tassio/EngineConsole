#-*- coding: utf-8 -*-

from PyQt4.QtCore import pyqtSignal

from engineConsole.base.engine import EngineConsole
from engineConsole.base.telaConsole import TelaConsole
from engineConsole.labelConsole import LabelConsole


class _ItemLista(TelaConsole):
    def __init__(self, tela, parent=None):
        super().__init__(parent)
        self._tela = tela
        self._selecionado = False

    def getTela(self):
        return self._tela

    def setSelecionado(self, sel):
        self._selecionado = sel

    def estaSelecionado(self):
        return self._selecionado

    def desenhoTela(self, tam):
        return '{0} {1}'.format([' ', '>'][self.estaSelecionado()], self._tela.desenhoTelaConsole(tam-2))


class ListaConsoleAbstrata(TelaConsole):
    selecaoModificada = pyqtSignal(str)
    itemSelecionado = pyqtSignal(object)
    HORIZONTAL = 0
    VERTICAL = 1
    def __init__(self, orientacao, parent=None):
        super().__init__(parent)
        self._itens = []
        self._orientacao = orientacao

    def getOrientacao(self):
        """Retorna a orientacao da lista"""
        return self._orientacao

    def setOrientacao(self, orientacao):
        """Modifica a orientacao da lista"""
        if self._orientacao != orientacao:
            self._orientacao = orientacao
            self.update()

    def clear(self):
        """Limpa os itens da lista"""
        self._itens = []

    def setIndexSelecionado(self, ind):
        """Modifica o indice selecionado"""
        if 0 <= ind < self.quantItens():
            if ind != self.indexSelecionado():
                self._itens[self.indexSelecionado()].setSelecionado(False)
                self._itens[ind].setSelecionado(True)
                self.selecaoModificada.emit(self.getItemSelecionado().getTexto())
                self.update()

    def indexSelecionado(self):
        """Retorna o indice selecionado"""
        for i in range(len(self._itens)):
            if self._itens[i].estaSelecionado():
                return i

        return -1

    def getItemSelecionado(self):
        """Retorna o item selecionado"""
        ind = self.indexSelecionado()
        if ind != -1:
            return self._itens[ind].getTela()

    def getTela(self, ind):
        return self._getItem(ind).getTela()

    def _getItem(self, ind):
        """Retorna o _ItemLista na posicao passada"""
        return self._itens[ind]

    def onEnter(self):
        item = self.getItemSelecionado()
        if item:
            self.itemSelecionado.emit(item)

    def onDirecional(self, direc):
        if self.quantItens() <= 1:
            return

        indSelecionado = self.indexSelecionado()
        if (self._orientacao == ListaConsoleAbstrata.VERTICAL and \
            direc == EngineConsole.UP) or \
           (self._orientacao == ListaConsoleAbstrata.HORIZONTAL and \
            direc == EngineConsole.LEFT):

            self.setIndexSelecionado(indSelecionado - 1)
        elif (self._orientacao == ListaConsoleAbstrata.VERTICAL and \
              direc == EngineConsole.DOWN) or \
             (self._orientacao == ListaConsoleAbstrata.HORIZONTAL and \
              direc == EngineConsole.RIGHT):

            self.setIndexSelecionado(indSelecionado + 1)

    def quantItens(self):
        """Retorna o numero de itens da lista"""
        return len(self._itens)

    def addItem(self, item):
        """Adiciona o item passado na lista"""
        itemLista = _ItemLista(item)
        if not self._itens:
            itemLista.setSelecionado(True)

        self._itens.append(itemLista)
        itemLista.setParent(self)
        self.update()

    def addItens(self, itens):
        """Adiciona os itens da lista passada nessa lista"""
        if not itens: return

        itensLista = [_ItemLista(i) for i in itens]
        if not self._itens:
            itensLista[0].setSelecionado(True)

        self._itens.extend(itensLista)
        for i in itensLista:
            i.setParent(self)
        self.update()

    def desenhoTela(self, tam):
        raise NotImplemented("Metodo abstrato")

    def acceptFocus(self):
        return True


class ListaTituloConsole(ListaConsoleAbstrata):
    def __init__(self, orientacao=ListaConsoleAbstrata.VERTICAL, titulo=LabelConsole("Lista", LabelConsole.CENTER), parent=None):
        super().__init__(orientacao, parent)
        self._titulo = None
        self.setTitulo(titulo)

    def setTitulo(self, titulo):
        if isinstance(titulo, TelaConsole):
            self._titulo = titulo
        else:
            raise TypeError("O titulo deve ser do tipo TelaConsole")

    def getTitulo(self):
        return self._titulo

    def _sinalCima(self):
        return ['<','^'][self.getOrientacao()==ListaConsoleAbstrata.VERTICAL]

    def _sinalBaixo(self):
        return ['>','v'][self.getOrientacao()==ListaConsoleAbstrata.VERTICAL]

    def _temMaisAcima(self):
        return self.indexSelecionado() > 0

    def _temMaisAbaixo(self):
        return self.indexSelecionado() < self.quantItens() - 1

    def _itensVisiveis(self):
        if self.quantItens() <= 4:
            return self._itens

        pos = self.indexSelecionado()

        if pos + 3 > self.quantItens():
            return self._itens[self.quantItens()-4:]
        elif pos - 2 < 0:
            return self._itens[:4]
        else:
            return self._itens[pos - 2: pos + 2]

    def desenhoTela(self, tam):
        s = '|{0:-<{1}}|\n'.format('',tam-2)
        s += '|{0:{1}}{2}{3}  {4}|\n'.format(self._titulo.desenhoTelaConsole(tam-7), tam-7, [' ',self._sinalCima()][self._temMaisAcima()], [' ',self._sinalBaixo()][self._temMaisAbaixo()], [' ','*'][self.hasFocus()])
        s += '|{0:-<{1}}|\n'.format('',tam-2)
        if self.getOrientacao() == ListaConsoleAbstrata.VERTICAL:
            for i in self._itensVisiveis():
                s += '|{0:{1}}|\n'.format(i.desenhoTelaConsole(tam-2), tam-2)
        else:
            lista = ''
            for i in self._itensVisiveis():
                lista += '{0:<{1}}'.format(i.desenhoTelaConsole(int((tam-2)/4)), int((tam-2)/4))
            s += '|{0:{1}}|\n'.format(lista, tam-2)

        s += '|{0:-<{1}}|'.format('',tam-2)
        return s


class MatrizConsole(ListaConsoleAbstrata):
    def __init__(self, numColunas=2, parent=None):
        super().__init__(ListaConsoleAbstrata.HORIZONTAL, parent=parent)
        self._numColunas = numColunas

    def setNumColunas(self, num):
        self._numColunas = num

    def numLinhas(self):
        return self.quantItens() / self._numColunas

    def onDirecional(self, direc):
        if direc == EngineConsole.UP:
            if self.indexSelecionado() - self._numColunas >= 0:
                self.setIndexSelecionado(self.indexSelecionado() - self._numColunas)
        elif direc == EngineConsole.DOWN:
            if self.indexSelecionado() + self._numColunas < self.quantItens():
                self.setIndexSelecionado(self.indexSelecionado() + self._numColunas)
        else:
            super().onDirecional(direc)

    def desenhoTela(self, tam):
        s = ''
        for i in range(0, self.quantItens(), self._numColunas):
            for j in range(i, min(self.quantItens(), i+self._numColunas)):
                s += '{0:<{1}}'.format(self._getItem(j).desenhoTelaConsole(int(tam/self._numColunas)), int(tam/self._numColunas))
            s += '\n'
        return s[:len(s)-1]

    
