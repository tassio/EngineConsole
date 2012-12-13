#-*- coding: utf-8 -*-

from engineConsole.base.telaConsole import TelaConsole


class PainelConsole(TelaConsole):
    """Classe que agrupa varias telas"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._childs = []

    def focusNextChild(self):
        """Passa o foco para o proximo filho"""
        ind = self.indexChildActive()
        if ind == -1 and self.acceptFocus() and self.isVisible() and not self.hasFocus():
            self.setFocus()
            return True

        ind = max(0, ind)
        for i in range(ind, len(self._childs)):
            if self._childs[i].isVisible() and self._childs[i].focusNextChild():
                return True

        return False

    def focusPreviousChild(self):
        """Passa o foco para o filho anterior"""
        ind = self.indexChildActive()
        for i in range(ind, 0, -1):
            if self._childs[i].isVisible() and self._childs[i].focusPreviousChild():
                return True
            
        if ind != -1 and self.acceptFocus() and self.isVisible() and not self.hasFocus():
            self.setFocus()
            return True

        return False

    def isParentOf(self, tela):
        """Verifica se a tela passada eh pai dessa"""
        if self.inChilds(tela):
            return True

        for i in self._childs:
            if i.isParentOf(tela):
                return True

        return False

    def indexChildActive(self):
        """Retorna o indice do filho ativo"""
        for i in range(len(self._childs)):
            if self._childs[i].activeWindow():
                return i
        return -1

    def addTela(self, tela):
        """Adiciona a tela no painel"""
        if tela:
            self._childs.append(tela)
            tela.setParent(self)
        else:
            raise TypeError("Tela nao pode ser None")

    def removeTela(self, tela):
        if tela in self._childs:
            self._childs.remove(tela)
            tela.setParent(None)

    def removeTelas(self):
        self._childs = []

    def getChilds(self):
        """Retorna as telas contidas no painel"""
        return self._childs

    def getChild(self, i):
        """Retorna as telas contidas no painel"""
        return self._childs[i] if 0 <= i < self.numTelas() else None

    def indexChild(self, child):
        return self.childs.index(child)

    def numTelas(self):
        """Retorna o numero de telas que estao no painel"""
        return len(self._childs)

    def desenhoTela(self, tam):
        s = ''
        for tela in self._childs:
            if tela.isVisible():
                s += tela.desenhoTelaConsole(tam) + '\n'

        if s.endswith('\n'):
            s = s[:len(s)-1]

        return s
    
