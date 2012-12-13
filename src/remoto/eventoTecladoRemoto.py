# -*- coding: utf-8 -*-
from networkService.servicos.servicoInformacao import ServicoInformacao
from engineConsole.base.eventoTeclado import EventoTeclado
from engineConsole.base.engine import Key
from networkService.servicos.informacao.registroInformacao import RegistroInformacao
from networkService.servicos.informacao.dataManipulador import DataManipulador
from networkService.servicos.informacao.informacao import InformacaoAbstrata


@RegistroInformacao.addInformacaoHandler(Key)
class KeyInformacao(InformacaoAbstrata):
    def __lshift__(self, data):
        m = DataManipulador(data)
        key = m.getNextInstance()
        code = m.getNextInstance()
        self.valor = Key((code, key))
        
    def __rshift__(self, data):
        m = DataManipulador(data)
        m.addInstance(self.valor.key)
        m.addInstance(self.valor.code)


class EventoTecladoRemotoReceber(EventoTeclado):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._servico = ServicoInformacao(40125, 40126)
        self._servico.pacoteInformacaoRecebida.connect(self._receberTecla)

    def _receberTecla(self, de, valor):
        self._entrarTecla(valor)


class EventoTecladoRemotoEnviar(EventoTeclado):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._servico = ServicoInformacao(40126, 40125)
        self._servico.setPara('127.0.0.1')
        
    def _entrarTecla(self, letra):
        super()._entrarTecla(letra)
        self._servico.enviarPacoteInformacao(letra)
