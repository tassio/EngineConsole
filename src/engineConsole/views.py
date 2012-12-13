#-*- coding: utf-8 -*-
from PyQt4.QtCore import pyqtSignal, QModelIndex, QAbstractTableModel, QAbstractListModel, Qt

from engineConsole.labelConsole import LabelConsole
from engineConsole.scrollConsole import AbstractScrollTela
from engineConsole.base.engine import EngineConsole


class AbstractViewTela(AbstractScrollTela):
    enterPressed = pyqtSignal()
    selecionadoModificado = pyqtSignal()
    def __init__(self, altura, parent=None):
        super().__init__(altura, parent)
        self._parent = QModelIndex()
        self._model = None
        self._selecionado = QModelIndex()

    def onDirecional(self, direc):
        s = self.getSelecionado()
        if direc == EngineConsole.UP:
            self.setSelecionado(self._model.index(s.row()-1, s.column(), s.parent()))
        elif direc == EngineConsole.DOWN:
            self.setSelecionado(self._model.index(s.row()+1, s.column(), s.parent()))

    def onEnter(self):
        self.enterPressed.emit()
        
    def setSelecionado(self, index):
        if not index.isValid() or index == self._selecionado:
            return

        self._selecionado = index
        self.deixarVisivelVertical(self.getNumLinhaSelecionado())
        self.selecionadoModificado.emit()
        self.update()

    def getSelecionado(self):
        return self._selecionado

    def getNumLinhaSelecionado(self):
        raise NotImplemented("Metodo abstrato")

    def getRootIndex(self):
        return self._parent

    def setRootIndex(self, index):
        if index.isValid():
            self._parent = index
            self.setSelecionado(self._model.index(0,0,self.getRootIndex()))

    def hasChildren(self, index):
        return False if isinstance(self._model, QAbstractTableModel) else self._model.hasChildren(index)

    def getNumLinhas(self, parent=None):
        if not parent:
            parent = self.getRootIndex()
            
        return self._model.rowCount(parent)

    def getNumColunas(self, parent=None):
        if not parent:
            parent = self.getRootIndex()
            
        return 1 if isinstance(self._model, QAbstractListModel) else self._model.columnCount(parent)

    def setModel(self, model):
        self._model = model
        self._model.dataChanged.connect(lambda ind1, ind2: self.update())
        self.setSelecionado(self._model.index(0,0,self.getRootIndex()))
        self.update()

    def getModel(self):
        return self._model


class ListViewTela(AbstractViewTela):
    def getNumLinhaSelecionado(self):
        return self.getSelecionado().row()
    
    def getDesenhoTela(self):
        s = []
        for i in range(self.getNumLinhas()):
            index = self._model.index(i,0,self.getRootIndex())
            s.append("{1}{0}".format(self._model.data(index), ' ' if index != self.getSelecionado() else '>'))

        return '\n'.join(s)


class TableViewTela(AbstractViewTela):
    LARGURA = 20
    def getNumLinhaSelecionado(self):
        return self.getSelecionado().row()
            
    def _adicionarLinhasFixas(self, tela):
        s = ' |'
        for i in range(self.getNumColunas()):
            valor = LabelConsole(str(self._model.headerData(i, Qt.Horizontal))).desenhoTelaConsole(TableViewTela.LARGURA-1)
            s += "{0:^{1}}|".format(valor, TableViewTela.LARGURA-1)
        s += '\n' + '-'*(TableViewTela.LARGURA*(self.getNumColunas())+2) + '\n'
        
        return s + tela
            
    def getDesenhoTela(self):
        s=''
        linhas = []
        for i in range(self.getNumLinhas()):
            linhas.append('{0}|'.format(' ' if self._model.index(i,0,self.getRootIndex()) != self.getSelecionado() else '>'))
            for j in range(self.getNumColunas()):
                valor = LabelConsole(str(self._model.data(self._model.index(i,j,self.getRootIndex())))).desenhoTelaConsole(TableViewTela.LARGURA-1)
                linhas[i] += '{0:<{1}}|'.format(valor, TableViewTela.LARGURA-1)
        
        s += '\n'.join(linhas)
        return s


class TreeViewTela(AbstractViewTela):
    LARGURA = 20
    def __init__(self, altura, parent=None):
        super().__init__(altura, parent)
        self._mostrarFilhos = set()

    def _numLinhasVisiveisAte(self, ate, parent):
        if (self.hasChildren(parent) and parent in self._mostrarFilhos) or parent == self.getRootIndex():
            linhas = 1
            for i in range(self._model.rowCount(parent)):
                index = self._model.index(i,0,parent)
                if index == ate:
                    break
                
                linhas += self._numLinhasVisiveisAte(None, index)
            return linhas
        else:
            return 1

    def getNumLinhaSelecionado(self):
        p = self.getSelecionado()
        i = -1
        while p != self.getRootIndex():
            i += self._numLinhasVisiveisAte(p, p.parent())
            p = p.parent()
        return i

    def addMostrarFilhos(self, index):
        self._mostrarFilhos.add(index)
        self.update()
    def removeMostrarFilhos(self, index):
        self._mostrarFilhos.remove(index)
        self.update()

    def onKey(self, key):
        if key == ' ':
            index = self.getSelecionado()
            if self.hasChildren(index):
                if index in self._mostrarFilhos:
                    self.removeMostrarFilhos(index)
                else:
                    self.addMostrarFilhos(index)
                
    def onDirecional(self, direc):
        s = self.getSelecionado()
        if direc == EngineConsole.RIGHT:
            if self.hasChildren(s):
                self.addMostrarFilhos(s)
                self.setSelecionado(s.child(0,0))
        elif direc == EngineConsole.LEFT:
            parent = s.parent()
            if parent.isValid():
                if parent == self.getRootIndex():
                    root = self.getRootIndex()
                    self.setRootIndex(parent.parent())
                    self.setSelecionado(root)
                    self.addMostrarFilhos(root)
                else:
                    self.setSelecionado(parent)
        super().onDirecional(direc)
                                    
    def _adicionarLinhasFixas(self, tela):
        s = ' | |'
        for i in range(self.getNumColunas()):
            valor = LabelConsole(str(self._model.headerData(i, Qt.Horizontal))).desenhoTelaConsole(TableViewTela.LARGURA-1)
            s += "{0:^{1}}|".format(valor, TableViewTela.LARGURA-1)
        s += '\n' + '-'*(TableViewTela.LARGURA*(self.getNumColunas())+4) + '\n'
        
        return s + tela

    def _desenhoArvore(self, parent, nivel=0):
        linhas = []
        for i in range(self.getNumLinhas(parent)):
            linhas.append('{0}|'.format(' ' if self._model.index(i,0,parent) != self.getSelecionado() else '>'))
            q = len(linhas)-1

            index = self._model.index(i,0,parent)
            hasChildren = self.hasChildren(index)
            
            linhas[q] += '{0} '.format(('-' if index in self._mostrarFilhos else '+') if hasChildren else ' ')
            for j in range(self.getNumColunas(parent)):
                if j == 0:
                    valor = '  '*nivel
                else:
                    valor = ''
                    
                valor = LabelConsole('{0}{1}'.format(valor, str(self._model.data(self._model.index(i,j,parent))))).desenhoTelaConsole(TableViewTela.LARGURA-1)
                linhas[q] += '{0:<{1}} '.format(valor, TableViewTela.LARGURA-1)
            linhas[q] = linhas[q][:len(linhas[q])-1] + '|'

            if hasChildren and index in self._mostrarFilhos:
                linhas.extend(self._desenhoArvore(self._model.index(i,0,parent), nivel+1).split('\n'))
                
        return '\n'.join(linhas)
            

    def getDesenhoTela(self):
        return self._desenhoArvore(self.getRootIndex())



