#-*- coding: utf-8 -*-

from engineConsole.base.telaConsole import TelaConsole


class ProgressBarConsole(TelaConsole):
    def __init__(self, mostrarTexto=True, tamanhoMaximo=30, parent=None):
        super().__init__(parent)
        self._mostrarTexto = mostrarTexto
        self._porcentagem = 0
        self._tamanhoMaximo = tamanhoMaximo

    def setPorcentagem(self, porc):
        porc = max(0, min(100, porc))
        if self._porcentagem != porc:
            self._porcentagem = porc
            self.update()

    def getPorcentagem(self):
        return self._porcentagem

    def _desenhoBarra(self, tam):
        barra = "="*int(tam*self.getPorcentagem()/100.)
        if self._porcentagem not in [0,100]:
            barra += '>'

        return "{0:<{1}}".format(barra,tam)

    def desenhoTela(self, tam):
        tamanhoMaxBarra = min(self._tamanhoMaximo, tam)-7
        return "[{0}] {1:<4}".format(self._desenhoBarra(tamanhoMaxBarra), str(self._porcentagem)+'%')
