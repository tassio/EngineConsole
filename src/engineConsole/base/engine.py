#-*- coding: utf-8 -*-
import string
#import WConio
import msvcrt
import os

class Key(object):
    def __init__(self, code_key=(None,None)):
        self.code, self.key = code_key
    
#TODO: Ajustar Engine Console para ser possivel escolher entre usar ou não o WConio
class EngineConsole(object):
    @staticmethod
    def clear():
        os.system("cls")#WConio.clrscr()
    @staticmethod
    def height():
        return 24#return WConio.gettextinfo()[3]+1
    @staticmethod
    def width():
        return 80#return WConio.gettextinfo()[2]+1
    @staticmethod
    def x():
        return WConio.wherex()
    @staticmethod
    def y():
        return WConio.wherey()
    @staticmethod
    def kbhit():
        return msvcrt.kbhit()#return WConio.kbhit()
    @staticmethod
    def readkey():
        tecla = msvcrt.getch().decode("cp1252")
        
        return Key((ord(tecla), tecla))#return Key(WConio.getch())
    @staticmethod
    def ungetch(ch):
        WConio.ungetch(ch)
    @staticmethod
    def goto(x,y):
        WConio.gotoxy(x, y)
    @staticmethod
    def printxy(x, y, texto):
        oldX, oldY = EngineConsole.x(), EngineConsole.y()
        EngineConsole.goto(x, y)
        print(texto)
        EngineConsole.goto(oldX, oldY)
    @staticmethod
    def move(left, top, right, bottom, x, y):
        WConio.movetext(left, top, right, bottom, x, y)
    @staticmethod
    def setTitle(title):
        WConio.settitle(title)
    @staticmethod
    def setTextColor(color):
        WConio.textcolor(color)

    SPACE = " "
    ENTER = '\r'
    ESC = '\x1b'
    TAB = '\t'
    BACKSPACE = '\x08'
    
    SINAL_INSERT = 82
    SINAL_HOME = 71
    SINAL_PAGEUP = 73
    SINAL_DELETE = 83
    SINAL_END = 79
    SINAL_PAGEDOWN = 81
    
    SINAIS_ESPECIAIS = (SINAL_INSERT, SINAL_HOME, SINAL_PAGEUP, \
                        SINAL_DELETE, SINAL_END, SINAL_PAGEDOWN)

    INSERT = "INSERT"
    HOME = "HOME"
    PAGEUP = "PAGEUP"
    DELETE = "DELETE"
    END = "END"
    PAGEDOWN = "PAGEDOWN"
    
    ESPECIAIS = (INSERT, HOME, PAGEUP, DELETE, END, PAGEDOWN)
    
    strings_printables = string.ascii_letters + ' ' + '0123456789' + 'áéíóúâêîôûãõàèìòùäëïöüÁÉÍÓÚÂÊÎÔÛÃÕÀÈÌÒÙÄËÏÖÜ' + 'çÇ' + string.punctuation + '´§ªº°¬¢£¹²³'
    
    SINAL_UP, SINAL_DOWN = 72, 80
    SINAL_LEFT, SINAL_RIGHT = 75, 77
    SINAIS_DIRECIONAIS = (SINAL_UP, SINAL_DOWN, SINAL_LEFT, SINAL_RIGHT)

    UP, DOWN, LEFT, RIGHT = '^', 'v', '<', '>'
    DIRECIONAIS = (UP, DOWN, LEFT, RIGHT)

    SINAL_F1, SINAL_F2, SINAL_F3, SINAL_F4 = 59, 60, 61, 62
    SINAL_F5, SINAL_F6, SINAL_F7, SINAL_F8 = 63, 64, 65, 66
    SINAL_F9, SINAL_F10 = 67, 68
    SINAIS_FUNCIONAIS = (SINAL_F1, SINAL_F2, SINAL_F3, SINAL_F4, \
                         SINAL_F5, SINAL_F6, SINAL_F7, SINAL_F8, \
                         SINAL_F9, SINAL_F10)

    F1, F2, F3, F4, F5 = "F1", "F2", "F3", "F4", "F5"
    F6, F7, F8, F9, F10 = "F6", "F7", "F8", "F9", "F10"
    FUNCIONAIS = (F1, F2, F3, F4, F5, \
                  F6, F7, F8, F9, F10)
    
