#-*- coding: utf-8 -*-

from PyQt4.QtCore import pyqtSignal, pyqtSlot

from engineConsole.base.engine import EngineConsole
from engineConsole.base.telaConsole import TelaConsole
from engineConsole.labelConsole import LabelConsole
from engineConsole.scrollConsole import AbstractScrollTela


class EditConsole(TelaConsole):
    enterPressed = pyqtSignal()
    posCursorAlterado = pyqtSignal(int)
    textoAlterado = pyqtSignal()
    def __init__(self, texto='', readOnly=False, parent=None):
        super().__init__(parent)
        self._readOnly = readOnly
        self._posCursor = 0
        self._texto = None
        self.setTexto(texto)

    def setTexto(self, texto):
        """Modifica o texto do Edit e atualiza o cursor para o final do texto"""
        if self._texto != texto:
            self._texto = texto
            self.setPosCursor(len(texto))
            self.update()

    def getTexto(self):
        return self._texto

    def getTextoComCursor(self):
        return self._texto[:self._posCursor] + '|' + self._texto[self._posCursor:]

    def appendTexto(self, texto):
        self.setTexto(self._texto + str(texto))

    def clear(self):
        """Limpa o texto do edit"""
        self.setTexto('')

    def setPosCursor(self, pos):
        """Se a posicão for maior que o tamanho do texto, posiciona o cursor no final do texto;
           Se a posição for menor que zero, posiciona o cursor no início do texto;
           Senão altera a posição do cursor no indice pedido"""
        pos =  max(0, min(pos, len(self._texto)))
        if self._posCursor != pos:
            self._posCursor = pos
            self.posCursorAlterado.emit(self._posCursor)
            self.update()

    def getPosCursor(self):
        return self._posCursor

    def onEnter(self):
        self.enterPressed.emit()

    def onKey(self, key):
        if key == EngineConsole.BACKSPACE:
            if self._posCursor > 0 and not self._readOnly:
                self._texto = self._texto[:self._posCursor-1] + self._texto[self._posCursor:]
                self.setPosCursor(self._posCursor - 1)
        elif key in EngineConsole.strings_printables:
            self.addLetraOnCursor(key)

    def setReadOnly(self, b):
        self._readOnly = b

    def addLetraOnCursor(self, letra):
        if self._readOnly:
            return

        self._texto = self._texto[:self._posCursor] + letra + self._texto[self._posCursor:]

        self._posCursor += 1
        self.update()

    def onDirecional(self, direc):
        if direc == EngineConsole.LEFT:
            self.setPosCursor(self._posCursor - 1)
        elif direc == EngineConsole.RIGHT:
            self.setPosCursor(self._posCursor + 1)

    def desenhoTela(self, tam):
        s = self.getTextoComCursor() if self.hasFocus() else self.getTexto()
        if len(s) > tam:
            s = s[:tam-3] + '...'

        return s

    def acceptFocus(self):
        return True


class TextEditConsole(AbstractScrollTela, EditConsole):
    #Redefinindo o sinal por problemas na herança múltipla
    posCursorAlterado = pyqtSignal(int)
    enterPressed = pyqtSignal()
    def __init__(self, numLinhas, texto='', parent=None):
        AbstractScrollTela.__init__(self, altura=numLinhas, parent=parent)
        EditConsole.__init__(self, texto=texto, parent=parent)

        self.posCursorAlterado.connect(self._ajustarPosScroll)

    @pyqtSlot(int)
    def _ajustarPosScroll(self, pos):
        self.deixarVisivelVertical(self.indLinhaAtual())
        self.deixarVisivelHorizontal(self.indColunaAtual())

    def numCaracteresAteLinha(self, linha):
        return sum(map(lambda t: len(t)+1, self.getTexto().split('\n')[:linha]))

    def indColunaAtual(self):
        return self.getPosCursor() - self.numCaracteresAteLinha(self.indLinhaAtual())

    def numColunas(self, linha):
        return len(self.getLinha(linha))-1

    def getLinha(self, i):
        if 0 <= i < self.numLinhas():
            return self.getTexto().split('\n')[i]

    def getLinhaAtual(self):
        return self.getLinha(self.linhaAtual())

    def indLinhaAtual(self):
        return (self.getTexto()[:self.getPosCursor()]).count('\n')

    def numLinhas(self):
        return self.getTexto().count('\n')+1

    def setLinhaColuna(self, linha, coluna):
        if 0 <= linha < self.numLinhas():
            coluna = min(self.numColunas(linha)+1, coluna)
            self.setPosCursor(self.numCaracteresAteLinha(linha)+coluna)

    def onDirecional(self, direc):
        linha = self.indLinhaAtual()
        coluna = self.indColunaAtual()
        if direc == EngineConsole.UP:
            self.setLinhaColuna(linha - 1, coluna)
        elif direc == EngineConsole.DOWN:
            self.setLinhaColuna(linha + 1, coluna)

        super().onDirecional(direc)

    def onEnter(self):
        self.addLetraOnCursor('\n')
        super().onEnter()

    def getDesenhoTela(self):
        return self.getTextoComCursor() if self.hasFocus() else self.getTexto()


class LabelEditConsole(EditConsole):
    def __init__(self, textoLabel='', texto='', parent=None):
        super().__init__(texto, parent)
        self._label = LabelConsole(textoLabel)

    def setTextoLabel(self, texto):
        self._label.setTexto(texto)

    def desenhoTela(self, tam):
        s = '{0}: '.format(self._label.desenhoTelaConsole(20))
        return s + super().desenhoTela(tam-len(s))

    
