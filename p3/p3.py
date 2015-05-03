from threading import Thread
import os
import inspect, re
import serial, time, json

if os.name == "posix":
    try:
        Serial = serial.Serial("/dev/ttyUSB0", 115200, timeout=0.1)	# *nix
    except:
        Serial = serial.Serial("/dev/ttyACM0", 115200, timeout=0.1)	# *pi
else:
    Serial = serial.Serial("com3", 115200, rtscts=0)		# windows->ard
#    Serial = serial.Serial("com3", 115200)		        # windows->ftdi

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
            print "\r\ncom->" + line.strip()

def OpenSerial():
    if Serial.isOpen():
        Serial.close()
    Serial.open()
    Thread(target=ReadSerial).start()

def CloseSerial():
    if Serial.isOpen():
        Serial.close()
        Thread(target=ReadSerial)._Thread__stop()

def printj(j):
    print "com<-" + str(j)

def Test1():
    j = json.dumps({"Cmd" : "Esc", "Value" : 1})
    printj(j)
    Serial.write(j + "\r\n")
    j = json.dumps({"Cmd" : "Power", "Value" : 40})
    printj(j)
    Serial.write(j + "\r\n")

    time.sleep(2)

    j = json.dumps({"Cmd" : "Power", "Value" : 0})
    printj(j)
    Serial.write(j + "\r\n")
    j = json.dumps({"Cmd" : "Esc", "Value" : 0})
    printj(j)    
    Serial.write(j + "\r\n")

    # +++ not working!
    #j = json.dumps({"Cmd" : "Reset", "H" : 90})
    #printj(j)
    #Serial.write(j + "\n")

def Heartbeat():
    print "Heartbeat"
    i = GetChoice([  "Off", "On 500", "On 1000", "On 5000", "On 20000" ])
    if i == 1:
        j = json.dumps({"Cmd" : "Heartbeat", "Value" :  1, "Int" : 500} )
    elif i == 2:
        j = json.dumps({"Cmd" : "Heartbeat", "Value" :  1, "Int" : 1000} )
    elif i == 3:
        j = json.dumps({"Cmd" : "Heartbeat", "Value" :  1, "Int" : 5000} )
    elif i == 4:
        j = json.dumps({"Cmd" : "Heartbeat", "Value" :  1, "Int" : 20000} )
    else:
        j = json.dumps({"Cmd" : "Heartbeat", "Value" :  0} )

    printj(j)
    Serial.write(j + "\n")

def Pid1():
    print "PID1"
    j = json.dumps({"Cmd" : "PID1",
                    "P" :  123.456, "I" :  123.456, "D" :  123.456 })
    printj(j)
    Serial.write(j + "\r\n")

def MotorMax():
    print "MotorMax"
    c = GetChoice(["20","40","60","80","100"])
    if c == 5:
        p = 100
    else:
        p = (c + 1) * 20
    j = json.dumps({"Cmd" : "MMax", "Value" : p })
    printj(j)
    Serial.write(j + "\n")

def SendGeom():
    j = json.dumps({"Cmd" : "Geom", "WB" : 140.00, "TPR" : 60, "WD" : 120.00})
    printj(j)
    Serial.write(j + "\n")
    
def ResetPose():
    j = json.dumps({"Cmd" : "Reset"})
    Serial.write(j + "\n")
    
def SetEsc():
    i = GetChoice([ "On", "Off" ])
    if i == 0:
        o = 1
    else:
        o = 0
    j = json.dumps({"Cmd" : "Esc", "Value" : o})
    printj(j)
    Serial.write(j + "\n")
    
def M1Sweep():
    # enable esc
    st = .5
    j = json.dumps({"Cmd" : "Esc", "Value" : 1})
    Serial.write(j + "\n")
    for p in xrange(0,101,10):
        j = json.dumps({"Cmd" : "Power", "Value" : p})
        printj(j)
        Serial.write(j + "\n")
        time.sleep(st)

    time.sleep(2);

    for p in xrange(100,-101,-10):
        j = json.dumps({"Cmd" : "Power", "Value" : p})
        printj(j)
        Serial.write(j + "\n")
        time.sleep(st)

    time.sleep(2);

    for p in xrange(-100,1,10):
        j = json.dumps({"Cmd" : "Power", "Value" : p})
        printj(j)
        Serial.write(j + "\n")
        time.sleep(st)

    # disable esc
    j = json.dumps({"Cmd" : "Esc", "Value" : 0})
    printj(j)
    Serial.write(j + "\n")

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
        print( "0) Exit")        
        k = getch()
        if k == '0':            
            return
        print
        if menu.has_key(k):
            if type(menu[k]) is dict:
                RunMenu(menu[k])
            else:
                if callable(menu[k]):
                    print menu[k].func_name
                    menu[k]()

PoseMenu = {
    '!' : "Pose",
    'r' : ResetPose,
    }

MotorMenu = {
    '!' : "Motor",
    'e' : SetEsc,
    'm' : MotorMax,
    's' : M1Sweep
    }

MainMenu = {
    '!' : "Main",
    '1' : OpenSerial,
    '9' : CloseSerial,
    't' : Test1,
    'p' : PoseMenu,
    'i' : Pid1,
    'm' : MotorMenu,
    'h' : Heartbeat,
    'g' : SendGeom,
    }


getch = _find_getch()
print("Python Pilot Test Suite .1")
RunMenu(MainMenu)
closing = True
CloseSerial()
print "\nBye\n"


