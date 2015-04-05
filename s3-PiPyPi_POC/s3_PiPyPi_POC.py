from colorama import Fore, Back, Style, init
from threading import Thread
import serial, time, json

Serial = serial.Serial("com4", 9600)
closing = False

def _find_getch():
    try:
        import termios
    except ImportError:
        # Non-POSIX. Return msvcrt's (Windows') getch.
        import msvcrt
        return msvcrt.getch

    # POSIX system. Create and return a getch that manipulates the tty.
    import sys, tty
    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    return _getch

def ReadSerial():
    while Serial.isOpen() and not closing:
        print(Serial.readline()),

def OpenSerial():
    if Serial.isOpen():
        Serial.close()
    Serial.open()
    Thread(target=ReadSerial).start()

def CloseSerial():
    if Serial.isOpen():
        Serial.close()
    Thread(target=ReadSerial).start()

def Test1():
    j = json.dumps({"Topic" : "Cmd/robot1", "T" : "Cmd", "Cmd" : "Test1"}, separators=(',',':') )
    #print j
    Serial.write(j)
    Serial.write("\n")

def EscEna():
    j = json.dumps({"Topic" : "Cmd/robot1", "T" : "Cmd", "Cmd" : "Esc", "Value" : "On"}, separators=(',',':') )
    #print j
    Serial.write(j)
    Serial.write("\n")

def EscDis():
    j = json.dumps({"Topic" : "Cmd/robot1", "T" : "Cmd", "Cmd" : "Esc", "Value" : "Off"}, separators=(',',':') )
    #print j
    Serial.write(j)
    Serial.write("\n")

def SendGeom():
    #j = json.dumps({"Topic" : "Cmd/robot1", "T" : "Cmd", "Cmd" : "Geom", "WheelBase" : 140.00})
    #print j
    #Serial.write(j)
    pass
    
def M1Sweep():
    # enable esc
    # for i=0 to 80 step
    # for i = 80 to -80 step -10
    # for i = -80 tp 0 step 10
    # disable esc
    pass

MainMenuMenu = {
    '1' : OpenSerial,
    '2' : Test1,
    '3' : EscEna,
    '4' : EscDis,
    '7' : SendGeom,
    '8' : M1Sweep,
    '9' : CloseSerial,
    }

def MainMenu():
    while True:
        for m in sorted(MainMenuMenu):
            print m + ")", MainMenuMenu[m].func_name
        print( "0) Exit")        
        k = getch()
        if k == '0':
            closing = True
            print(Fore.WHITE + Back.MAGENTA + "Exit" + Fore.RESET + Back.RESET)
            if Serial.isOpen():
                Serial.close()
            return
        print(Fore.WHITE + Back.GREEN + MainMenuMenu[k].func_name + Fore.RESET + Back.RESET)
        MainMenuMenu[k]()


getch = _find_getch()
init()  # colorama
print(Fore.WHITE + Back.GREEN + "Python Pilot Test Suite .1" + Fore.RESET + Back.RESET + Style.RESET_ALL)
MainMenu()

