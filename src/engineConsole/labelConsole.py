#-*- coding: utf-8 -*-

from engineConsole.base.telaConsole import TelaConsole


class LabelConsole(TelaConsole):
    RIGHT = ">"
    CENTER = "^"
    LEFT = "<"
    ALIGNMENT = [RIGHT, CENTER, LEFT]
    def __init__(self, texto='', align="<", parent=None):
        super().__init__(parent)
        self._texto = texto
        self._alignment = str()
        self.setAlignment(align)

    def setAlignment(self, align):
        """Modifica o alinhamento do texto no label"""
        if align in LabelConsole.ALIGNMENT:
            self._alignment = align
        else:
            raise Exception("Alinhamento invalido: {0}".format(align))

    def getAlignment(self):
        """Retorna o alinhamento do texto no label"""
        return self._alignment

    def setTexto(self, texto):
        """Modifica o texto do label"""
        if self._texto != texto:
            self._texto = texto
            self.update()

    def getTexto(self):
        """Retorna o texto do label"""
        return self._texto

    def desenhoTela(self, tam):
        s = []
        for i in self._texto.split('\n'):
            s.append('{0:{1}{2}}'.format(i[:tam-3] + '...' if len(i) > tam else i, self._alignment, tam if self._alignment != LabelConsole.LEFT else ''))

        return '\n'.join(s)
