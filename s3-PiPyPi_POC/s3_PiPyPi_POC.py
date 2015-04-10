from colorama import Fore, Back, Style, init
from threading import Thread
import serial, time, json

Serial = serial.Serial("/dev/ttyUSB0", 115200)	# *nix
#Serial = serial.Serial("com4", 115200)		# windows

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
        print(Serial.readline())

def OpenSerial():
    if Serial.isOpen():
        Serial.close()
    Serial.open()
    Thread(target=ReadSerial).start()

def CloseSerial():
    if Serial.isOpen():
        Serial.close()
    Thread(target=ReadSerial)._Thread__stop()

def Test1():
    j = json.dumps({"Topic" : "Cmd/robot1", "T" : "Cmd", "Cmd" : "Test1"} )
    #print j
    Serial.write(j + "\n")

def SendGeom():
    j = json.dumps({"Topic" : "Cmd/robot1", "T" : "Cmd", "Cmd" : "Geom", "WheelBase" : 140.00, "TicksPerRevo" : 60, "WheelBase" : 120})
    #print j
    Serial.write(j + "\n")
    
def SetPose():
    j = ""
    c = Choice(["On", "Off"])
    if  c == '1':
        j = json.dumps({"Topic" : "Cmd/robot1", "T" : "Cmd", "Cmd" : "Pose", "Value" : "On"})
    elif c == '2':
        j = json.dumps({"Topic" : "Cmd/robot1", "T" : "Cmd", "Cmd" : "Pose", "Value" : "Off"})    
    Serial.write(j + "\n")
    
def SetEsc():
    j = ""
    c = Choice(["On", "Off"])
    if  c == '1':
        j = json.dumps({"Topic" : "Cmd/robot1", "T" : "Cmd", "Cmd" : "Esc", "Value" : "On"})
    elif c == '2':
        j = json.dumps({"Topic" : "Cmd/robot1", "T" : "Cmd", "Cmd" : "Esc", "Value" : "Off"})
    print j	
    Serial.write(j + "\n")
    
def M1Sweep():
    # enable esc
    # for i=0 to 80 step
    # for i = 80 to -80 step -10
    # for i = -80 tp 0 step 10
    # disable esc
    pass

def Choice(a):
    for i in xrange(len(a)):
        print str(i+1) + ")", a[i]        
    k = getch()
    print(Fore.WHITE + Back.BLUE + a[int(k)-1] + Fore.RESET + Back.RESET)
    return k

def RunMenu(menu):
    while True:
        for m in sorted(menu):
            print m + ")", menu[m].func_name
        print( "0) Exit")        
        k = getch()
        if k == '0':
            print(Fore.WHITE + Back.YELLOW + "Exit" + Fore.RESET + Back.RESET)
            return
        print
        print(Fore.WHITE + Back.GREEN + MainMenuMenu[k].func_name + Fore.RESET + Back.RESET)
        menu[k]()
        print

def PoseMenu():
    RunMenu(PoseMenuMenu)

def MotorMenu():
    RunMenu(MotorMenuMenu);

PoseMenuMenu = {
    '1' : SetPose,
    }

MotorMenuMenu = {
    '1' : SetEsc,
    '3' : M1Sweep
    }

MainMenuMenu = {
    '1' : OpenSerial,
    '2' : Test1,
    '3' : PoseMenu,
    '4' : MotorMenu,
    '7' : SendGeom,
    '9' : CloseSerial,
    }


getch = _find_getch()
init()  # colorama
print(Fore.WHITE + Back.GREEN + "Python Pilot Test Suite .1" + Fore.RESET + Back.RESET + Style.RESET_ALL)
RunMenu(MainMenuMenu)
closing = True
if Serial.isOpen():
    Serial.close()

