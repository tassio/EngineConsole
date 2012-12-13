#-*- coding: utf-8 -*-

from engineConsole.painelConsole import PainelConsole


class VLayoutConsole(PainelConsole):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._porcentagens = []
        self._alinhamentos = []

    def addTela(self, porc, tela, alinhamento="<"):
        total = sum(self._porcentagens)
        if total == 100:
            raise Exception("VLayoutTela::addTela: O layout ja esta completo. Essa tela nao sera adicionada!")

        if porc=="*" or porc + total > 100:
            porc = 100 - total

        super().addTela(tela)
        self._porcentagens.append(porc)
        self._alinhamentos.append(alinhamento)

    def removeTela(self, tela):
        if tela in self.getChilds():
            ind = self.indexChild(tela)
            self._porcentagens.pop(ind)
            self._alinhamentos.pop(ind)
            super().removeTela(tela)

    def desenhoTela(self, tam):
        telas = []
        for i in range(self.numTelas()):
            tamanho = int(tam*self._porcentagens[i]/100.)
            telas.append(self.getChild(i).desenhoTelaConsole(tamanho).split('\n'))

        s = ''
        for i in range(max(map(len, telas))):
            for j in range(self.numTelas()):
                tamanho = int(tam*self._porcentagens[j]/100.)
                alinhamento = self._alinhamentos[j]
                if i < len(telas[j]):
                    s += '{0:{1}{2}}'.format(str(telas[j][i]), alinhamento, tamanho)
                else:
                    s += '{0:{1}}'.format('', tamanho)
            s+='\n'

        if s.endswith('\n'):
            s = s[:len(s)-1]

        return s

    
