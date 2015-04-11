from threading import Thread
import os
import inspect, re
import serial, time, json

if os.name == "posix":
    Serial = serial.Serial("/dev/ttyUSB0", 115200)	# *nix
else:
    Serial = serial.Serial("com4", 115200)		# windows

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

def varname(p):
  for line in inspect.getframeinfo(inspect.currentframe().f_back)[3]:
    m = re.search(r'\bvarname\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)', line)
    if m:
      return m.group(1)

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

def Heartbeat():
    i = GetChoice([ "On 500", "On 1000", "Off" ])
    if i == 1:
        j = json.dumps({"Topic" : "Cmd/robot1", "T" : "Cmd", "HB" : 1, "Int" : 500} )
    elif i == 2:
        j = json.dumps({"Topic" : "Cmd/robot1", "T" : "Cmd", "HB" : 1, "Int" : 500} )
    else:
        j = json.dumps({"Topic" : "Cmd/robot1", "T" : "Cmd", "HB" : 0} )

    print j
    Serial.write(j + "\n")

def SendGeom():
    j = json.dumps({"Topic" : "Cmd/robot1", "T" : "Cmd", "Cmd" : "Geom", "WheelBase" : 140.00, "TicksPerRevo" : 60, "WheelBase" : 120})
    #print j
    Serial.write(j + "\n")
    
def SetPose():
    j = ""
    c = OnOff()
    j = json.dumps({"Topic" : "Cmd/robot1", "T" : "Cmd", "Cmd" : "Pose", "Value" : c})
    Serial.write(j + "\n")
    
def SetEsc():
    j = ""
    c = OnOff()
    j = json.dumps({"Topic" : "Cmd/robot1", "T" : "Cmd", "Cmd" : "Esc", "Value" : c})
    # print j
    Serial.write(j + "\n")
    
def M1Sweep():
    # enable esc
    j = json.dumps({"Topic" : "Cmd/robot1", "T" : "Cmd", "Cmd" : "Esc", "Value" : 1})
    Serial.write(j + "\n")
    # for i=0 to 80 step 10
    # for i = 80 to -80 step -10
    # for i = -80 tp 0 step 10    
    # disable esc
    j = json.dumps({"Topic" : "Cmd/robot1", "T" : "Cmd", "Cmd" : "Esc", "Value" : 0})
    Serial.write(j + "\n")

def GetChoice(choices):
    for i in xrange(len(choices)):
        print str(i+1) + ")", choices[i]        
    k = int(getch())
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
                # RunMenu(m[1])
        print( "0) Exit")        
        k = getch()
        if k == '0':
            # print("Exit")
            return
        print
        if type(menu[k]) is dict:
            RunMenu(menu[k])
        else:
            menu[k]()
        print


PoseMenu = {
    '!' : "Pose",
    's' : SetPose,
    }

MotorMenu = {
    '!' : "Motor",
    'e' : SetEsc,
    's' : M1Sweep
    }

MainMenu = {
    '!' : "Main",
    's' : OpenSerial,
    't' : Test1,
    'p' : PoseMenu,
    'm' : MotorMenu,
    'h' : Heartbeat,
    'g' : SendGeom,
    'x' : CloseSerial,
    }


getch = _find_getch()
print("Python Pilot Test Suite .1")
RunMenu(MainMenu)
closing = True
if Serial.isOpen():
    Serial.close()

