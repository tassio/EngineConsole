#-*- coding: utf-8 -*-

from PyQt4.QtCore import QEvent


class EventoUpdateConsole(QEvent):
    UpdateRequest = QEvent.registerEventType(1250)
    UpdateLaterRequest = QEvent.registerEventType(1251)
