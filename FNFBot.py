import pyautogui as p
import ctypes
import time
import threading

leftPos = (770,160)
downPos = (895, 160)
upPos = (1000,160)
rightPos = (1130,160)

leftHoldPos = (787,186)
downHoldPos = (894,193)
upHoldPos = (1005,200)
rightHoldPos = (1114,186)

leftCol = (194,75,153)
downCol = (0,255,255)
upCol = (18,250,5)
rightCol = (249,57,63)

leftHoldCol = (141,64,117)
downHoldCol = (25,172,179)
upHoldCol = (30,165,23)
rightHoldCol = (174,53,63)

SendInput = ctypes.windll.user32.SendInput

# C struct redefinitions 
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseLeft():
    ReleaseKey(30)
def ReleaseDown():
    ReleaseKey(31)
def ReleaseUp():
    ReleaseKey(17)
def ReleaseRight():
    ReleaseKey(32)


while True:
    try:
        #left arrow
        if p.pixelMatchesColor(leftPos[0],leftPos[1],leftCol):
            PressKey(30)
        else:
            leftPixel = p.pixel(leftHoldPos[0],leftHoldPos[1])
            if leftPixel[0] < 150 and leftPixel[2] < 150:
                leftDelay = threading.Timer(.2,ReleaseLeft)
                leftDelay.start()

        #down arrow
        if p.pixelMatchesColor(downPos[0],downPos[1],downCol):
            PressKey(31)
        elif p.pixel(downHoldPos[0],downHoldPos[1])[2] < 150:
            downDelay = threading.Timer(.2,ReleaseDown)
            downDelay.start()

        #up arrow
        if p.pixelMatchesColor(upPos[0],upPos[1],upCol):
            PressKey(17)
        elif p.pixel(upHoldPos[0],upHoldPos[1])[1] < 150:
            upDelay = threading.Timer(.2,ReleaseUp)
            upDelay.start()

        #right arrow
        if p.pixelMatchesColor(rightPos[0],rightPos[1],rightCol):
            PressKey(32)                   
        elif p.pixel(rightHoldPos[0],rightHoldPos[1])[0] < 150:
            rightDelay = threading.Timer(.2,ReleaseRight)
            rightDelay.start()


    except OSError:
        print("OS Error")
