#-*- coding: utf-8 -*-

from engineConsole.base.telaConsole import TelaConsole


class SpacerConsole(TelaConsole):
    def __init__(self, numLinhas, parent=None):
        super().__init__(parent)
        self._numLinhas = numLinhas

    def setNumLinhas(self, num):
        self._numLinhas = num

    def getNumLinhas(self):
        return self._numLinhas

    def desenhoTela(self, tam):
        return ' \n'*self._numLinhas
