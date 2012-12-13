# -*- coding: utf-8 -*-

from engineConsole.base.baseApplication import CApplication
from engineConsole.base.telaConsole import TelaConsole

from remoto.eventoTecladoRemoto import EventoTecladoRemotoReceber,\
    EventoTecladoRemotoEnviar
from networkService.servicos.servicoInformacao import ServicoInformacao


class CApplicationReceber(CApplication):
    class Tela(TelaConsole):
        def __init__(self, texto='', parent=None):
            super().__init__(parent)
            self._texto = texto
        def setTexto(self, texto):
            self._texto = texto
            self.update()
        def desenhoTela(self, tam):
            return self._texto
    
    def __init__(self, parent=None):
        super().__init__(desenharBorda=False, parent=parent)
        self._servico = ServicoInformacao(40132, 40133)
        self._servico.setPara('127.0.0.1')
        self._servico.pacoteInformacaoRecebida.connect(self._receberTela)
        self._tela = CApplicationReceber.Tela('Esperando Receber Tela')
        self._tela.show()
        self.setEventoTeclado(EventoTecladoRemotoEnviar())

    def _receberTela(self, de, valor):
        self._tela.setTexto(valor)


class CApplicationEnviar(CApplication):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._servico = ServicoInformacao(40133, 40132)
        self._servico.setPara('127.0.0.1')
        self.setEventoTeclado(EventoTecladoRemotoReceber())
        self.telaAtualizada.connect(self._enviarTela)

    def _enviarTela(self):
        self._servico.enviarPacoteInformacao(CApplicationEnviar._getDesenhoTela())
