#-*- coding: utf-8 -*-

from PyQt4.QtCore import QEvent


class EventoFocusConsole(QEvent):
    FocusIn = QEvent.registerEventType(1270)
    FocusOut = QEvent.registerEventType(1271)
