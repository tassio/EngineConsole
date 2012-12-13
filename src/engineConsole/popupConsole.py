#-*- coding: utf-8 -*-

from engineConsole.base.baseApplication import CApplication
from engineConsole.base.telaConsole import TelaConsole


class PopupConsole(TelaConsole):
    """Tela que eh aberta por cima da aplicacao principal.
        Tudo volta ao normal quando esta eh fechada."""
    def __init__(self, tela, parent=None):
        super().__init__(parent)
        self._telaPopup = tela
        self._telaFocada = None
        self._telaPrincipal = None

    def focusNextChild(self):
        return self._telaPopup.focusNextChild()

    def focusPreviousChild(self):
        return self._telaPopup.focusPreviousChild()

    def onEsc(self):
        self.close()

    def show(self):
        self._telaFocada = CApplication.getTelaFocada()
        self._telaPrincipal = CApplication.getTelaPrincipal()
        self._telaPrincipal.setVisible(False)

        CApplication.hideTelaPrincipal()
        self._telaPopup.show()
        CApplication.setFocus(None)
        self.focusNextChild()

    def close(self):
        CApplication.hideTelaPrincipal()
        self._telaPrincipal.setVisible(True)
        self._telaPrincipal.show()
        CApplication.setFocus(self._telaFocada)
