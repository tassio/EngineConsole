#-*- coding: utf-8 -*-
from PyQt4.QtCore import QCoreApplication, QObject, pyqtSignal

from engineConsole.base.controladorConsole import EventoTecladoConsoleDispatcher
from engineConsole.base.engine import EngineConsole
from engineConsole.base.eventoFocus import EventoFocusConsole
from engineConsole.base.eventoUpdate import EventoUpdateConsole
from engineConsole.base.eventoTeclado import EventoTeclado
import traceback


class CApplication(QObject):
    """Loop de eventos da aplicacao no console"""
    telaAtualizada = pyqtSignal()

    _APP = None
    _TELAS = []
    _TELA_FOCADA = None
    _TELA_PRINCIPAL = None
    _CONTROLADOR_EVENTOS = None
    _DESENHAR_BORDA = True
    _INSTANCE = None
    _DESENHO_TELA_ATUAL = ''

    _UPDATE_REQUESTED = False
    
    def __init__(self, app=None, desenharBorda=True, event=None, parent=None):
        super().__init__(parent)
        if CApplication._INSTANCE:
            raise Exception("Nao podem existir duas CApplications")
        CApplication._INSTANCE = self

        CApplication._CONTROLADOR_EVENTOS = EventoTecladoConsoleDispatcher(eventoTeclado=event)
        CApplication._APP = app if app != None else QCoreApplication([])
        CApplication._DESENHAR_BORDA = desenharBorda

    @staticmethod
    def getInstance():
        """Retorna a instancia criada do CApplication"""
        return CApplication._INSTANCE

    def setEventoTeclado(self, event):
        """Modifica a thread que ira pegar os eventos do teclado"""
        CApplication._CONTROLADOR_EVENTOS.setEventoTeclado(event)

    @staticmethod
    def getTelaFocada():
        """Retorna a tela que esta com o foco"""
        return CApplication._TELA_FOCADA
    
    @staticmethod
    def setFocus(tela):
        """Passa o foco para a tela especificada"""
        oldFocus = CApplication.getTelaFocada()
        CApplication._TELA_FOCADA = tela
        CApplication._CONTROLADOR_EVENTOS.setTela(tela)
        CApplication.sendFocusEvent(oldFocus, tela)

    @staticmethod
    def setFocusTelaPrincipal():
        CApplication._TELA_FOCADA = None
        CApplication._TELA_PRINCIPAL.focusNextChild()

    @staticmethod
    def sendFocusEvent(oldFocus, newFocus):
        if oldFocus != newFocus:
            if oldFocus:
                QCoreApplication.postEvent(oldFocus, EventoFocusConsole(EventoFocusConsole.FocusOut))
            if newFocus:
                QCoreApplication.postEvent(newFocus, EventoFocusConsole(EventoFocusConsole.FocusIn))

    @staticmethod
    def getTelaPrincipal():
        """Retorna a tela principal"""
        return CApplication._TELA_PRINCIPAL
    
    @staticmethod
    def setTelaPrincipal(tela):
        """Modifica a tela principal da aplicacao"""
        if CApplication._TELA_PRINCIPAL:
            raise Exception("O método show de outra tela já foi chamado.\n \
                             OBS: Chame o método hide da tela que está visível antes de chamar o show de qualquer outra")
        CApplication._TELA_PRINCIPAL = tela
            
    @staticmethod
    def hideTelaPrincipal():
        """Esconde a tela principal"""
        CApplication._TELA_PRINCIPAL = None

    @staticmethod
    def updateApp():
        """Atualiza a aplicação"""
        if not CApplication._UPDATE_REQUESTED:
            CApplication._UPDATE_REQUESTED = True
            QCoreApplication.postEvent(CApplication.getInstance(), EventoUpdateConsole(EventoUpdateConsole.UpdateRequest))
    
    @staticmethod
    def _updateTela():
        """Atualiza a tela principal"""
        try:
            CApplication._DESENHO_TELA_ATUAL = CApplication._getDesenhoTela()
        except Exception:
            CApplication._DESENHO_TELA_ATUAL = "Exceção lançada durante a renderização da tela:\n\n{0}".format(traceback.format_exc())
        
        CApplication._INSTANCE.telaAtualizada.emit()
            
        # Atualizando a tela
        EngineConsole.clear()
        print(CApplication._DESENHO_TELA_ATUAL)
    
    @staticmethod
    def getScreenshot():
        """Retorna um screenshot da tela naquele momento"""
        tela = CApplication.getDesenhoTelaAtual()
        saida = ''
        for i in range(0, len(tela), EngineConsole.width()):
            saida += tela[i:min(i+EngineConsole.width(), len(tela))] + '\n'
        return saida

    @staticmethod
    def getDesenhoTelaAtual():
        """Retorna o desenho da tela atual"""
        return CApplication._DESENHO_TELA_ATUAL

    @staticmethod
    def salvarScreenshot(path):
        """Salva um screenshot da tela no arquivo"""
        with open(path, 'w') as arq:
            print(CApplication.getScreenshot(), file=arq)

    @staticmethod
    def _getDesenhoTela():
        """Retorna a tela ja formatada para ser mostrada"""
        tam = EngineConsole.width()
        if CApplication._DESENHAR_BORDA:
            tam -= 2

        tela = CApplication._TELA_PRINCIPAL.desenhoTelaConsole(tam)
        return CApplication._ajustarTela(tela)
    
    @staticmethod
    def _ajustarTela(tela):
        """Ajusta a tela de acordo com o valor de _DESENHA_BORDA"""
        if CApplication._DESENHAR_BORDA:
            return CApplication._desenharBordaTela(tela)
        else:
            newTela = ''
            for linha in tela.split('\n'):
                newTela += '{0:<{1}}'.format(linha, EngineConsole.width())
            return newTela
    
    @staticmethod
    def _desenharBordaTela(tela):
        """Retorna a tela com a borda"""
        newTela = ' /' + '-'*(EngineConsole.width()-4) + '\\ '
        for linha in tela.split('\n'):
            newTela += '|{0:<{1}}|'.format(linha, EngineConsole.width()-2)

        for _i in range(EngineConsole.height()-3-len(tela.split('\n'))):
            newTela += '|{0:<{1}}|'.format('', EngineConsole.width()-2)
            
        newTela += ' \\' + '-'*(EngineConsole.width()-4) + '/'
        return newTela

    @staticmethod
    def registrarTela(tela):
        """Adiciona a tela na lista de telas da aplicacao"""
        CApplication._TELAS.append(tela)
    
    @staticmethod
    def allTelas():
        """Retorna todas as telas da aplicacao"""
        return CApplication._TELAS
    
    def customEvent(self, event):
        if event.type() == EventoUpdateConsole.UpdateRequest:
            CApplication._updateTela()
            CApplication._UPDATE_REQUESTED = False
            QCoreApplication.removePostedEvents(CApplication.getInstance(), EventoUpdateConsole.UpdateRequest)
    
    def exec_(self):
        """Inicia a Thread que manipula os eventos do teclado e a atualizacao da tela e executa a aplicacao"""
        if not CApplication._TELA_PRINCIPAL:
            raise Exception("Deve ser chamado o metodo show de alguma Tela antes de executar a aplicacao")

        if not CApplication._CONTROLADOR_EVENTOS.getEventoTeclado():
            CApplication._CONTROLADOR_EVENTOS.setEventoTeclado(EventoTeclado())
            
        CApplication._CONTROLADOR_EVENTOS.start()
        CApplication.setFocusTelaPrincipal()
        CApplication._TELA_PRINCIPAL.update()
        
        return CApplication._APP.exec_()

    def exit(self):
        """Sai da aplicacao"""
        CApplication._CONTROLADOR_EVENTOS.stop()
        CApplication._APP.exit()
