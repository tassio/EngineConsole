#-*- coding: utf-8 -*-
from PyQt4.QtCore import QCoreApplication

from engineConsole.base.eventoTeclado import EventListener, EventoTecladoConsole
from engineConsole.base.engine import EngineConsole


class EventoTecladoConsoleDispatcher(EventListener):
    def __init__(self, tela=None, eventoTeclado=None):
        super().__init__()
        self._tela = tela
        self._eventoTeclado = eventoTeclado

    def setTela(self, tela):
        self._tela = tela

    def setEventoTeclado(self, evento):
        self._eventoTeclado = evento

    def getEventoTeclado(self):
        return self._eventoTeclado

    def start(self):
        self._eventoTeclado.addListener(self)
        self._eventoTeclado.start()

    def stop(self):
        self._eventoTeclado.stop()
        
    def onKey(self, key):
        if not self._tela:
            return
        
        evento = EventoTecladoConsole(EventoTecladoConsole.KeyType, key)
        QCoreApplication.sendEvent(self._tela, evento)

    def onEnter(self):
        if not self._tela:
            return

        evento = EventoTecladoConsole(EventoTecladoConsole.EnterType, EngineConsole.ENTER)
        QCoreApplication.sendEvent(self._tela, evento)
        
    def onEscape(self):
        if not self._tela:
            return

        evento = EventoTecladoConsole(EventoTecladoConsole.EscapeType, EngineConsole.ESC)
        QCoreApplication.sendEvent(self._tela, evento)
        
    def onDirecional(self, direc):
        if not self._tela:
            return

        evento = EventoTecladoConsole(EventoTecladoConsole.DirecionalType, direc)
        QCoreApplication.sendEvent(self._tela, evento)
        
    def onFuncional(self, func):
        if not self._tela:
            return

        evento = EventoTecladoConsole(EventoTecladoConsole.FuncionalType, func)
        QCoreApplication.sendEvent(self._tela, evento)
        
    def onEspecial(self, esp):
        if not self._tela:
            return 
        
        evento = EventoTecladoConsole(EventoTecladoConsole.EspecialType, esp)
        QCoreApplication.sendEvent(self._tela, evento)

    def onTab(self):
        if not self._tela:
            return

        evento = EventoTecladoConsole(EventoTecladoConsole.TabType, EngineConsole.TAB)
        QCoreApplication.sendEvent(self._tela, evento)
