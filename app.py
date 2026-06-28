import sys
import tkinter as tk
from tkinter import font as tkfont
import json
import ctypes
import time
from ctypes import wintypes
import pydirectinput


pydirectinput.PAUSE = 0.0

settings = None
with open("settings.json", "r") as file:
    settings = json.load(file)

HMIDIIN = wintypes.HANDLE
CALLBACK_FUNCTION = 0x00030000
MIM_DATA = 0x3C3
winmm = ctypes.WinDLL('winmm.dll')


MIDI_MAP = {
    # === OKTAV 1 ===
    36: ('1', False),  # C  -> 1
    37: ('1', True),   # C# -> ! (Shift + 1)
    38: ('2', False),  # D  -> 2
    39: ('2', True),   # D# -> @ (Shift + 2)
    40: ('3', False),  # E  -> 3
    41: ('4', False),  # F  -> 4
    42: ('4', True),   # F# -> $ (Shift + 4)
    43: ('5', False),  # G  -> 5
    44: ('5', True),   # G# -> % (Shift + 5)
    45: ('6', False),  # A  -> 6
    46: ('6', True),   # A# -> ^ (Shift + 6)
    47: ('7', False),  # H  -> 7

    # === OKTAV 2 ===
    48: ('8', False),  # C  -> 8
    49: ('8', True),   # C# -> * (Shift + 8)
    50: ('9', False),  # D  -> 9
    51: ('9', True),   # D# -> ( (Shift + 9)
    52: ('0', False),  # E  -> 0
    53: ('q', False),  # F  -> q
    54: ('q', True),   # F# -> Q (Shift + q)
    55: ('w', False),  # G  -> w
    56: ('w', True),   # G# -> W (Shift + w)
    57: ('e', False),  # A  -> e
    58: ('e', True),   # A# -> E (Shift + e)
    59: ('r', False),  # H  -> r

    # === OKTAV 3 ===
    60: ('t', False),  # C  -> t
    61: ('t', True),   # C# -> T (Shift + t)
    62: ('y', False),  # D  -> y
    63: ('y', True),   # D# -> Y (Shift + y)
    64: ('u', False),  # E  -> u
    65: ('i', False),  # F  -> i
    66: ('i', True),   # F# -> I (Shift + i)
    67: ('o', False),  # G  -> o
    68: ('o', True),   # G# -> O (Shift + o)
    69: ('p', False),  # A  -> p
    70: ('p', True),   # A# -> P (Shift + p)
    71: ('a', False),  # H  -> a

    # === OKTAV 4 ===
    72: ('s', False),  # C  -> s
    73: ('s', True),   # C# -> S (Shift + s)
    74: ('d', False),  # D  -> d
    75: ('d', True),   # D# -> D (Shift + d)
    76: ('f', False),  # E  -> f
    77: ('g', False),  # F  -> g
    78: ('g', True),   # F# -> G (Shift + g)
    79: ('h', False),  # G  -> h
    80: ('h', True),   # G# -> H (Shift + h)
    81: ('j', False),  # A  -> j
    82: ('j', True),   # A# -> J (Shift + j)
    83: ('k', False),  # H  -> k

    # === OKTAV 5 ===
    84: ('l', False),  # C  -> l
    85: ('l', True),   # C# -> L (Shift + l)
    86: ('z', False),  # D  -> z
    87: ('z', True),   # D# -> Z (Shift + z)
    88: ('x', False),  # E  -> x
    89: ('c', False),  # F  -> c
    90: ('c', True),   # F# -> C (Shift + c)
    91: ('v', False),  # G  -> v
    92: ('v', True),   # G# -> V (Shift + v)
    93: ('b', False),  # A  -> b
    94: ('b', True),   # A# -> B (Shift + b)
    95: ('n', False),  # H  -> n

    # === SISTE TANGENT (TOPP-C) ===
    96: ('m', False),  # C  -> m
}

root = tk.Tk("M2Q")
root.geometry("1080x720")
root.config(bg=settings["color"]["bg"])

Bold16 = tkfont.Font(family=settings["font"], weight="bold", size=16)
Regular16 = tkfont.Font(family=settings["font"], weight="normal", size=16)

PixI = tk.PhotoImage(width=1, height=1)

topBar = tk.Frame(root, bg=settings["color"]["bg2"], height=100)
topBar.pack(fill=tk.X, side=tk.TOP)

def close():
    sys.exit(0)

exitBtn = tk.Button(topBar, text="X", command=close, bg=settings["color"]["fg"], fg=settings["color"]["bg2"], image=PixI, compound="center", height=25, width=25, relief="flat", font=Bold16)
exitBtn.pack(side=tk.RIGHT)

fullscreen = False
def toggleFullscreen(event=None):
    global fullscreen
    fullscreen = not fullscreen
    root.attributes("-fullscreen", fullscreen)
    if fullscreen:
        FSBtn.config(text="🗖")
    else:
        FSBtn.config(text="⤢")

TOpen = True
def toggleTerminal(event=None):
    global TOpen
    TOpen = not TOpen
    if TOpen:
        terminalBtn.config(text="Hide")
        terminalBtn.place(relheight=0.02, relwidth=0.02, rely=0.775, relx=0.975)
        terminal.place(relheight=0.2, relwidth=1, rely=0.80)
    else:
        terminalBtn.config(text="Show")
        terminalBtn.place(relheight=0.02, relwidth=0.02, rely=0.975, relx=0.975)
        terminal.place_forget()

root.bind("<F11>", toggleFullscreen)

FSBtn = tk.Button(topBar, text="⤢", command=toggleFullscreen, bg=settings["color"]["fg"], fg=settings["color"]["bg2"], image=PixI, compound="center", height=25, width=25, relief="flat", font=Bold16)
FSBtn.pack(side=tk.RIGHT)

title = tk.Label(topBar, text="M2Q", relief="flat", width=5, bg=settings["color"]["bg2"], fg=settings["color"]["fg"], font=Bold16)
title.pack(side=tk.LEFT, fill=tk.Y)

terminal = tk.Frame(root, bg=settings["color"]["bg2"])
terminal.place(relheight=0.2, relwidth=1, rely=0.80)

terminalBtn = tk.Button(root, command=toggleTerminal, text="Hide", bg=settings["color"]["fg"], fg=settings["color"]["bg2"], image=PixI, compound="center", height=25, width=25, relief="flat", font=Bold16)
terminalBtn.place(relheight=0.02, relwidth=0.02, rely=0.775, relx=0.975)

T1 = tk.Label(terminal, bg=settings["color"]["bg"], fg=settings["color"]["fg2"], font=Regular16, justify="left", anchor="w", text="No key pressed yet")
T1.place(relheight=0.2, relwidth=0.998, relx=0.001, rely=0.01)
T2 = tk.Label(terminal, bg=settings["color"]["bg"], fg=settings["color"]["fg2"], font=Regular16, justify="left", anchor="w")
T3 = tk.Label(terminal, bg=settings["color"]["bg"], fg=settings["color"]["fg2"], font=Regular16, justify="left", anchor="w")
T4 = tk.Label(terminal, bg=settings["color"]["bg"], fg=settings["color"]["fg2"], font=Regular16, justify="left", anchor="w")
T5 = tk.Label(terminal, bg=settings["color"]["bg"], fg=settings["color"]["fg2"], font=Regular16, justify="left", anchor="w")

M1 = "No key pressed yet"
M2 = None
M3 = None
M4 = None
M5 = None

def send_directx_press(key_char, shift_required):
    """Sender tastetrykket på lavt nivå slik at Roblox forstår det."""
    if shift_required:
        pydirectinput.keyDown('shift')
        time.sleep(0.001)
    
    pydirectinput.keyDown(key_char)
    time.sleep(0.015)  # Tid tasten holdes nede i millisekunder
    pydirectinput.keyUp(key_char)
    
    if shift_required:
        time.sleep(0.001)
        pydirectinput.keyUp('shift')

# Windows C-Callback for MIDI-meldinger
MIDIINPROC = ctypes.WINFUNCTYPE(None, HMIDIIN, wintypes.UINT, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)

@MIDIINPROC
def midi_callback(hMidiIn, wMsg, dwInstance, dwParam1, dwParam2):
    if wMsg == MIM_DATA:
        status = dwParam1 & 0xFF
        raw_note = (dwParam1 >> 8) & 0xFF
        velocity = (dwParam1 >> 16) & 0xFF
        
        event_type = status & 0xF0
        
        # Note On (Tangent trykkes ned)
        if event_type == 0x90 and velocity > 0:
            calibrated_note = raw_note + settings["midiOffset"]
            
            if calibrated_note in MIDI_MAP:
                key_char, shift_required = MIDI_MAP[calibrated_note]

                global T1
                global T2
                global T3
                global T4
                global T5

                global M1
                global M2
                global M3
                global M4
                global M5
                M5 = M4
                M4 = M3
                M3 = M2
                M2 = M1
                M1 = f"🎵 MIDI: {raw_note} -> QWERTY: '{key_char.upper() if shift_required else key_char}' (Shift={shift_required})"
                T1.config(text=M1)
                if M2:
                    T2.place(relheight=0.2, relwidth=0.998, relx=0.001, rely=0.22)
                    T2.config(text=M2)
                if M3:
                    T3.place(relheight=0.2, relwidth=0.998, relx=0.001, rely=0.43)
                    T3.config(text=M3)
                if M4:
                    T4.place(relheight=0.2, relwidth=0.998, relx=0.001, rely=0.64)
                    T4.config(text=M4)
                if M5:
                    T5.place(relheight=0.2, relwidth=0.998, relx=0.001, rely=0.85)
                    T5.config(text=M5)
                send_directx_press(key_char, shift_required)

# --- START LYTTING ---
num_devices = winmm.midiInGetNumDevs()
if num_devices == 0:
    print("Ingen MIDI-enheter funnet. Sjekk tilkoblingen.")
    exit()

hMidiIn = HMIDIIN()
winmm.midiInOpen(ctypes.byref(hMidiIn), 0, midi_callback, 0, CALLBACK_FUNCTION)
winmm.midiInStart(hMidiIn)

root.mainloop()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nAvslutter...")
finally:
    winmm.midiInStop(hMidiIn)
    winmm.midiInClose(hMidiIn)
