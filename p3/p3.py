from threading import Thread
import os
import inspect, re
import serial, time, json

# long overdue updates to get back in sync

Serial = None
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
        line = Serial.readline()
        if line:
            print "com->" + line.strip()

def OpenSerial():
    global Serial
    if Serial != None and Serial.isOpen():
        Serial.close()
    if os.name == "posix":
        try:
            Serial = serial.Serial("/dev/ttyUSB0", 115200, timeout=0.1)	# *nix
        except:
            Serial = serial.Serial("/dev/ttyACM0", 115200, timeout=0.1)	# *pi
    else:
        Serial = serial.Serial("com7", 115200, rtscts=0)		# windows->ard

    closing = False

    Thread(target=ReadSerial).start()

def SendPilot(j):
    j2 = json.dumps(j)
    print "com<-" + str(j2)
    Serial.write(j2 + "\n")


def CloseSerial():
    if Serial.isOpen():
        Serial.close()
        Thread(target=ReadSerial)._Thread__stop()

#---------------------------------------------   

def ResetPose():
    SendPilot({"Cmd" : "RESET"})

def SendConfig():
#   Pilot.Send(new { Cmd = "CONFIG", Geom = new float[] { 336.2F,  450 } });

    SendPilot({"Cmd" : "CONFIG", "Geom" : [ 336.2,  450.0] })
    
def SetEsc():
    i = GetChoice([ "On", "Off" ])
    if i == 0:
        o = 1
    else:
        o = 0
    SendPilot({"Cmd" : "ESC", "Value" : o})

def DistanceTest():
    SendPilot({"Cmd" : "PWR", "Dist" : 2.0, "M1" : 40.0, "M2" : 40.0 })
    
def MotorStop():
    SendPilot({"Cmd" : "PWR", "M1" : 0, "M2" : 0 })
    
#------------------------------------------------------

def GetChoice(choices):
    for i in xrange(len(choices)):
        print str(i + 1) + ")", choices[i]        
    k = int(getch()) - 1
    print choices[k]
    return k 

def RunMenu(menu):
    print(">> " + menu['!'])
    while True:
        for m in sorted(menu):
            if callable(menu[m]):
                print  m + ") " + menu[m].func_name
            elif type(menu[m]) is dict:
                print  m + ") " + menu[m]["!"]                
        print( "z) Exit")        
        k = getch()
        if k == 'z' or k == 'Z':            
            return
        print
        if menu.has_key(k):
            if type(menu[k]) is dict:
                RunMenu(menu[k])
            else:
                if callable(menu[k]):
                    print menu[k].func_name
                    menu[k]()

MotorMenu = {
    '!' : "Motor",
    'x' : MotorStop,
    'e' : SetEsc,
    'd' : DistanceTest,
    }

MainMenu = {
    '!' : "Main",
    '1' : OpenSerial,
    '9' : CloseSerial,
    'c' : SendConfig,
    'r' : ResetPose,
    'm' : MotorMenu,
    }

getch = _find_getch()
print("Python Pilot Test Suite .3")
RunMenu(MainMenu)
closing = True
CloseSerial()
print "\nBye\n"


