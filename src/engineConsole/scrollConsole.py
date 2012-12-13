#-*- coding: utf-8 -*-
from PyQt4.QtCore import pyqtSignal, QRect

from engineConsole.base.engine import EngineConsole
from engineConsole.base.telaConsole import TelaConsole
from engineConsole.base.eventoTeclado import EventoTecladoConsole


class ScrollBarConsole(TelaConsole):
    HORIZONTAL = 0
    VERTICAL = 1
    valorScrollModificado = pyqtSignal(int)
    def __init__(self, tamanho, ateValor, passo=1, orientacao=1, parent=None):
        """tamanho = numero de '-' ou '|' na barra mais as '<>' ou 'v^'. Ex: "<-> tamanho = 3", "<-    > tamanho = 7"
           ateValor = Numero de passos ate do inicio ate o final da barra
        """
        super().__init__(parent)

        self._tamanho = None
        self.setTamanho(tamanho)

        self._valorAtual = 0
        self._ateValor = ateValor
        self._passo = passo
        self._orientacao = orientacao

    def setTamanho(self, tamanho):
        if tamanho > 2:
            self._tamanho = tamanho
        else:
            raise Exception("O tamanho da barra deve ser maior que 2")

    def setAteValor(self, valor):
        if self._ateValor != valor:
            self._ateValor = valor
            self._valorAtual = min(self._valorAtual, self._ateValor)
            self.update()

    def getAteValor(self):
        return self._ateValor

    def setValorAtual(self, valor):
        v = max(0, min(valor, self._ateValor))
        if self._valorAtual != v:
            self._valorAtual = v
            self.valorScrollModificado.emit(self._valorAtual)
            self.update()

    def getValorAtual(self):
        return self._valorAtual

    def onDirecional(self, direc):
        if (self._orientacao == ScrollBarConsole.HORIZONTAL and direc == EngineConsole.RIGHT) or \
           (self._orientacao == ScrollBarConsole.VERTICAL and direc == EngineConsole.DOWN):
            self.setValorAtual(self._valorAtual + self._passo)
        elif (self._orientacao == ScrollBarConsole.HORIZONTAL and direc == EngineConsole.LEFT) or \
             (self._orientacao == ScrollBarConsole.VERTICAL and direc == EngineConsole.UP):
            self.setValorAtual(self._valorAtual - self._passo)

    def acceptFocus(self):
        return True

    def desenhoTela(self, tam):
        tamBarra = self._tamanho - 2
        numBarras = max(1, min(tamBarra-1, int(float(tamBarra) / self._ateValor)+1)) if self._ateValor != 0 else tamBarra
        espaco = int((tamBarra-numBarras)*float(self._valorAtual / self._ateValor)) if self._ateValor != 0 else tamBarra - numBarras

        if self._orientacao == ScrollBarConsole.HORIZONTAL:
            barra = ' '*espaco + "-"*numBarras
            s = "<{0:<{1}}>".format(barra, tamBarra)
        else:
            barra = ' \n'*espaco + "|\n"*numBarras + " \n"*(tamBarra-espaco-numBarras)
            s = "^\n{0}v".format(barra)

        return s


class AbstractScrollTela(TelaConsole):
    def __init__(self, altura, parent=None):
        super().__init__(parent=parent)

        self._rectTela = QRect(0,0,0,altura)
        self._mostrarHorizontal = False
        self._mostrarVertical = False

        self._scrollHorizontal = ScrollBarConsole(3,0,orientacao=ScrollBarConsole.HORIZONTAL,parent=self)
        self._scrollVertical = ScrollBarConsole(self._rectTela.height(),0,orientacao=ScrollBarConsole.VERTICAL,parent=self)

        self._scrollHorizontal.valorScrollModificado.connect(self._moverHorizontal)
        self._scrollVertical.valorScrollModificado.connect(self._moverVertical)

        self._scrollBarFocus = ScrollBarConsole(3,0,parent=self)
        self._scrollBarFocus.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == self._scrollBarFocus and event.type() != EventoTecladoConsole.TabType:
            self._scrollVertical.customEvent(event)
            self._scrollHorizontal.customEvent(event)
            return True
        else:
            return False

    def acceptFocus(self):
        return True

    def focusNextChild(self):
        if self._scrollBarFocus.hasFocus():
            return False

        if self.hasFocus():
            if not (self._mostrarVertical or self._mostrarHorizontal):
                return False
            self._scrollBarFocus.setFocus()
        else:
            if not self.acceptFocus():
                return False
            self.setFocus()

        return True

    def focusPrevChild(self):
        if self.hasFocus():
            return False

        if self._scrollBarFocus.hasFocus():
            if self.acceptFocus():
                self.setFocus()
            else:
                return False
        else:
            self._scrollBarFocus.setFocus()
        return True
    
    def indexChildActive(self):
        if self._scrollBarFocus.hasFocus():
            return 0
        
        return -1

    def getRectTela(self):
        return self._rectTela

    def _moverVertical(self, valor):
        self._scrollVertical.setValorAtual(valor)
        self._rectTela.moveTop(valor)

    def _moverHorizontal(self, valor):
        self._scrollHorizontal.setValorAtual(valor)
        self._rectTela.moveLeft(valor)

    def deixarVisivelVertical(self, valor):
        top = self.getRectTela().top()
        height = self.getRectTela().height() - self._numLinhasFixas() - 1
        bottom = top + height

        if valor < top:
            self._moverVertical(valor)
        elif valor > bottom:
            self._moverVertical(valor - height)

    def deixarVisivelHorizontal(self, valor):
        left = self.getRectTela().left()
        width = self.getRectTela().width()-1
        right = left + width

        if valor < left:
            self._moverHorizontal(valor)
        elif valor > right:
            self._moverHorizontal(valor - width)

    def scrollContentsBy(self, dx, dy):
        self._rectTela.translate(dx,dy)

    def getDesenhoTela(self):
        raise NotImplemented("Metodo abstrato")

    def _adicionarScrollBar(self, tela):
        if self._mostrarVertical:
            tela = self._adicionarScrollVertical(tela)

        if self._mostrarHorizontal:
            tela = self._adicionarScrollHorizontal(tela)

        return tela

    def _adicionarScrollVertical(self, texto):
        scroll = ''
        for i in self._scrollVertical.desenhoTelaConsole(self._rectTela.width()).split('\n'):
            scroll += "{0}|\n".format(i)
        scroll = "-|\n{0}-|".format(scroll).split('\n')

        s = ''
        texto = texto.split('\n')
        for i in range(len(texto)):
            s += "{0:{1}}{2}\n".format(texto[i], self._rectTela.width()+2, scroll[i])

        if s.endswith('\n'):
            s = s[:len(s)-1]

        return s

    def _adicionarScrollHorizontal(self, texto):
        texto += '\n|{0}|{1}\n'.format(self._scrollHorizontal.desenhoTelaConsole(self._rectTela.width()), 'X|' if self._mostrarVertical else '')
        texto += '|{0:-<{1}}|{2}'.format('', self._rectTela.width(), '-|' if self._mostrarVertical else '')
        return texto

    def _ajustarScroll(self, tela):
        linhas = tela.split('\n')
        numColunas = max(map(len, linhas))
        numLinhasFixas = self._numLinhasFixas()
        numLinhas = len(linhas) + numLinhasFixas

        self._mostrarVertical = numLinhas > self._rectTela.height()
        self._mostrarHorizontal = numColunas > self._rectTela.width()

        self._scrollHorizontal.setAteValor(max(0, numColunas-self._rectTela.width()))
        self._scrollVertical.setAteValor(max(0, numLinhas-self._rectTela.height()))

    def _adicionarLinhasFixas(self, tela):
        """Esse método deve ser sobrescrito pela classe filha para adicionar as linhas fixas na tela"""
        return tela

    def _numLinhasFixas(self):
        return self._adicionarLinhasFixas('').count('\n')

    def _linhasVisiveis(self, tela):
        linhas = tela.split('\n')
        numLinhasFixas = self._numLinhasFixas()
        numLinhas = len(linhas) + numLinhasFixas

        if numLinhas < self._rectTela.height():
            tela = self._adicionarLinhasFixas(tela)
            tela += '\n'*(self._rectTela.height()-numLinhas)
        else:
            top = self.getRectTela().top()
            bottom = self.getRectTela().bottom()+1
            return self._adicionarLinhasFixas('\n'.join(linhas[top:bottom - numLinhasFixas]))

        return tela

    def _colunasVisiveis(self, tela):
        linhas = tela.split('\n')
        numColunas = max(map(len, linhas))+1

        if numColunas > self._rectTela.width():
            tela = '\n'.join([linha[self._rectTela.left():self._rectTela.right()+1] for linha in linhas])

        return tela

    def _ajustarTela(self, tela):
        tela = self._linhasVisiveis(tela)
        tela = self._colunasVisiveis(tela)
        return tela

    def desenhoTela(self, tam):
        tela = self.getDesenhoTela()
        self._ajustarScroll(tela)

        if self._mostrarVertical:
            tam -= 2

        if tam-2 != self._rectTela.width():
            self._rectTela.setWidth(tam-2)
            self._scrollHorizontal.setTamanho(tam-2)
            self._ajustarScroll(tela)

        tela = self._ajustarTela(tela)
        tela = self._colocarBorda(tela, tam)
        return self._adicionarScrollBar(tela)


class ScrollTela(AbstractScrollTela):
    def __init__(self, tela, altura, parent=None):
        super().__init__(altura, parent)

        self.setTela(tela)

    def setTela(self, tela):
        self._tela = tela
        self._tela.setParent(self)
        self.update()

    def getTela(self):
        return self._tela

    def getDesenhoTela(self):
        return self._tela.desenhoTelaConsole(80)
