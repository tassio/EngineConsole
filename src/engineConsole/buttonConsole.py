#-*- coding: utf-8 -*-

from PyQt4.QtCore import pyqtSignal

from engineConsole.base.telaConsole import TelaConsole
from engineConsole.base.engine import EngineConsole
from engineConsole.base.eventoTeclado import EventoTecladoConsole
from engineConsole.painelConsole import PainelConsole


class AbstractButtonConsole(TelaConsole):
    enterPressed = pyqtSignal()
    def __init__(self, texto="", parent=None):
        super().__init__(parent)
        self._texto = texto
        self._enabled = True
        
    def setTexto(self, texto):
        """Modifica o texto do botao"""
        if self._texto != texto:
            self._texto = texto
            self.update()
            
    def getTexto(self):
        return self._texto
        
    def setEnabled(self, b):
        self._enabled = b
        
    def isEnabled(self):
        return self._enabled
    
    def onEnter(self):
        self.enterPressed.emit()
    
    def acceptFocus(self):
        return self._enabled
    
    
class AbstractCheckableButtonConsole(AbstractButtonConsole):
    checked = pyqtSignal(bool)
    def __init__(self, texto='', parent=None):
        super().__init__(texto, parent)

        self._checked = False
        
    def setChecked(self, checked):
        if self._checked != checked:
            self._checked = checked
            self.checked.emit(checked)
        
    def isChecked(self):
        return self._checked


class ButtonConsole(AbstractButtonConsole):
    def desenhoTela(self, tam):
        if not self.isEnabled():
            sinal = '-'
        elif self.hasFocus():
            sinal = '+'
        else:
            sinal = ' '

        s = '{1}{0}{1}'.format(self._texto, sinal)

        if len(s) > tam:
            s = s[:tam-3] + '...'
        
        return s

    
class CheckBoxConsole(AbstractCheckableButtonConsole):   
    def customEvent(self, event):
        if (event.type() == EventoTecladoConsole.KeyType and event.tecla() == EngineConsole.SPACE) or event.type() == EventoTecladoConsole.EnterType:
            self.setChecked(not self._checked)
            self.update()
        
        super().customEvent(event)
         
    def desenhoTela(self, tam):
        if not self.isEnabled():
            sinal = "-"
        elif self.isChecked():
            sinal = "X"
        else:
            sinal = " "
            
        s = '{2}[{1}] {0}'.format(self._texto, sinal, self.hasFocus() and "*" or " ")
        
        if len(s) > tam:
            s = s[:tam-3] + '...'
        
        return s
    

class RadioButtonConsole(AbstractCheckableButtonConsole):
    def customEvent(self, event):
        if (event.type() == EventoTecladoConsole.KeyType and event.tecla() == EngineConsole.SPACE) or event.type() == EventoTecladoConsole.EnterType:
            if not self.isChecked():
                self.setChecked(True)
                self.update()
        
        super().customEvent(event)
        
    def desenhoTela(self, tam):
        if not self.isEnabled():
            sinal = "-"
        elif self.isChecked():
            sinal = "O"
        else:
            sinal = " "
            
        s = '{2}({1}) {0}'.format(self._texto, sinal, self.hasFocus() and "*" or " ")
        
        if len(s) > tam:
            s = s[:tam-3] + '...'
        
        return s
    

class PainelBotoesConsole(PainelConsole):
    def addButton(self, texto):
        """Adiciona um botao ao painel e retorna o botao adicionado"""
        b = ButtonConsole(texto)
        self.addTela(b)
        return b

    def desenhoTela(self, tam):
        des = []
        for i in self.getChilds():
            if i.isVisible():
                des.append(i.desenhoTelaConsole(80))

        tamanho = tam - len(''.join(des))
        espacamento = ' '*int(tamanho / (self.numTelas()+1))

        s = espacamento
        for i in des:
            s += i + espacamento

        return s
        
        