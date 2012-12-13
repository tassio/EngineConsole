# -*- coding: utf-8 -*-
from PyQt4.QtCore import pyqtSignal, QThread, QObject, QEvent

from engineConsole.base.engine import EngineConsole


class EventoTecladoBase(QThread):
    keyPressed = pyqtSignal(str)
    enterPressed = pyqtSignal()
    escapePressed = pyqtSignal()
    tabPressed = pyqtSignal()
    funcionalPressionada = pyqtSignal(str)
    especialPressionada = pyqtSignal(str)
    direcionalPressionada = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)

        self._direc = bytes()
        self._func = bytes()
        self.start()
        
    def _entrarTecla(self, tecla):
        if tecla.code in (0, 224):
            code = EngineConsole.readkey().code
            self._entrarTeclaEspecial(code)
        else:
            self._entrarLetra(tecla)

    def _entrarLetra(self, k):
        self.keyPressed.emit(k.key)

        if k.key == EngineConsole.ENTER:
            self.enterPressed.emit()
        elif k.key == EngineConsole.ESC:
            self.escapePressed.emit()
        elif k.key == EngineConsole.TAB:
            self.tabPressed.emit()
            
    def _entrarTeclaEspecial(self, code):
        if code in EngineConsole.SINAIS_DIRECIONAIS:
            indice = EngineConsole.SINAIS_DIRECIONAIS.index(code)
            self.direcionalPressionada.emit(EngineConsole.DIRECIONAIS[indice])
        elif code in EngineConsole.SINAIS_FUNCIONAIS:
            indice = EngineConsole.SINAIS_FUNCIONAIS.index(code)
            self.funcionalPressionada.emit(EngineConsole.FUNCIONAIS[indice])
        elif code in EngineConsole.SINAIS_ESPECIAIS:
            indice = EngineConsole.SINAIS_ESPECIAIS.index(code)
            self.especialPressionada.emit(EngineConsole.ESPECIAIS[indice])

    def addListener(self, l):
        if isinstance(l, EventListener):
            self.keyPressed.connect(l.onKey)
            self.escapePressed.connect(l.onEscape)
            self.enterPressed.connect(l.onEnter)
            self.tabPressed.connect(l.onTab)
            self.direcionalPressionada.connect(l.onDirecional)
            self.especialPressionada.connect(l.onEspecial)
            self.funcionalPressionada.connect(l.onFuncional)
        else:
            raise TypeError("Argumento tem tipo inválido. Deve ser um EventListener")
            

class EventoTeclado(EventoTecladoBase):
    def run(self):
        while 1:
            if EngineConsole.kbhit():
                self._entrarTecla(EngineConsole.readkey())
                
            self.msleep(20)


class EventListener(QObject):
    def onKey(self, key):
        pass
    def onEnter(self):
        pass
    def onEscape(self):
        pass
    def onDirecional(self, direc):
        pass
    def onFuncional(self, func):
        pass
    def onEspecial(self, esp):
        pass
    def onTab(self):
        pass


class EventoTecladoConsole(QEvent):
    KeyType = QEvent.registerEventType(1122)
    EscapeType = QEvent.registerEventType(1123)
    EnterType = QEvent.registerEventType(1124)
    DirecionalType = QEvent.registerEventType(1125)
    FuncionalType = QEvent.registerEventType(1126)
    EspecialType = QEvent.registerEventType(1127)
    TabType = QEvent.registerEventType(1128)
    def __init__(self, tipo, tecla):
        super().__init__(tipo)
        self._tecla = tecla
    def tecla(self):
        return self._tecla
    
