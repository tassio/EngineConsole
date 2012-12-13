#-*- coding: utf-8 -*-
from PyQt4.QtCore import QObject

from engineConsole.base.baseApplication import CApplication
from engineConsole.base.eventoTeclado import EventoTecladoConsole
from engineConsole.base.eventoFocus import EventoFocusConsole


class _TelaFocus(object):
    def setFocus(self):
        if self.acceptFocus():
            CApplication.setFocus(self)
    def focusNextChild(self):
        if not self.hasFocus() and self.acceptFocus():
            self.setFocus()
            return True
        
        return False
    def focusPreviousChild(self):
        if not self.hasFocus() and self.acceptFocus():
            self.setFocus()
            return True
        
        return False
    
    def hasFocus(self):
        return CApplication.getTelaFocada() == self
    def acceptFocus(self):
        return False
    def indexChildActive(self):
        return -1
    def activeWindow(self):
        return self.hasFocus() or self.indexChildActive() != -1


class TelaConsole(QObject, _TelaFocus):
    def __init__(self, parent=None):
        super().__init__(parent)
        CApplication.registrarTela(self)
        self._visible = True
    
    def setVisible(self, visible):
        self._visible = visible
        self.update()
        
    def isVisible(self):
        parent = self.parent()
        if parent:
            return self._visible and parent.isVisible()
        else:
            return self._visible #and self == CApplication.getTelaPrincipal()
        
    def customEvent(self, event):
        if event.type() == EventoTecladoConsole.KeyType:
            self.onKey(event.tecla())
        elif event.type() == EventoTecladoConsole.EscapeType:
            self.onEscape()
        elif event.type() == EventoTecladoConsole.EnterType:
            self.onEnter()
        elif event.type() == EventoTecladoConsole.DirecionalType:
            self.onDirecional(event.tecla())
        elif event.type() == EventoTecladoConsole.FuncionalType:
            self.onFuncional(event.tecla())
        elif event.type() == EventoTecladoConsole.EspecialType:
            self.onEspecial(event.tecla())
        elif event.type() == EventoTecladoConsole.TabType:
            tela = self
            while tela:
                if tela.focusNextChild():
                    break
                tela = tela.parent()
            else:
                CApplication.setFocusTelaPrincipal()
            
        elif event.type() == EventoFocusConsole.FocusIn:
            self.onFocusIn(event)
        elif event.type() == EventoFocusConsole.FocusOut:
            self.onFocusOut(event)

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
    def onFocusIn(self, event):
        self.update()
    def onFocusOut(self, event):
        self.update()
        
    def focusNextChild(self):
        if not self.isVisible():
            return False
        
        return super().focusNextChild()
    def focusPreviousChild(self):
        if not self.isVisible():
            return False
        
        return super().focusPreviousChild()

    def isParentOf(self, tela):
        return False
    def inChilds(self, tela):
        return tela in self.getChilds()
    def getChilds(self):
        return []
    def show(self):
        CApplication.setTelaPrincipal(self)
    def hide(self):
        CApplication.hideTelaPrincipal()
    def update(self):
        if self.isVisible():
            CApplication.updateApp()

    def _colocarBorda(self, texto, tam):
        s = "|{0:-<{1}}|\n".format('', tam-2)
        for i in texto.split('\n'):
            s += "|{0:<{1}}|\n".format(i, tam-2)
        s += "|{0:-<{1}}|".format('', tam-2)
        return s

    
    def desenhoTelaConsole(self, tam):
        if not self.isVisible():
            return ''

        return self.desenhoTela(tam)
        
    def desenhoTela(self, tam):
        return ''
