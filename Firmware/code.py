import time
import board
import digitalio
import usb_hid

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

#assign keyboard and computer controls
kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)


#order the pins
key_pins = {
    "1": board.A2,
    "2": board.A3,
    "3": board.SCK,

    "4": board.A0,
    "5": board.TX,
    "6": board.MISO,

    "7": board.A1,
    "8": board.RX,
    "9": board.MOSI,
}



actions = {
    "1": ("keycode", [Keycode.CONTROL, Keycode.T]),        
    "2": ("media", ConsumerControlCode.PLAY_PAUSE),        
    "3": ("keycode", [Keycode.WINDOWS, Keycode.L]),  

    "4": ("keycode", [Keycode.CONTROL, Keycode.C]),     
    "5": ("keycode", [Keycode.CONTROL, Keycode.V]),     
    "6": ("keycode", [Keycode.CONTROL, Keycode.X]),     

    "7": ("keycode", [Keycode.DOWN_ARROW]),               
    "8": ("keycode", [Keycode.UP_ARROW]),               
    "9": ("keycode", [Keycode.ENTER]),                     
}


buttons = {}

for key, pin in key_pins.items():
    btn = digitalio.DigitalInOut(pin)
    btn.direction = digitalio.Direction.INPUT
    btn.pull = digitalio.Pull.UP
    buttons[key] = btn


#main loop
last_pressed = set()

while True:
    pressed = set()


    for key, btn in buttons.items():
        if not btn.value: 
            pressed.add(key)


    new_keys = pressed - last_pressed

    for key in new_keys:
        if key in actions:
            action_type, value = actions[key]

            if action_type == "keycode":
                kbd.send(*value)

            elif action_type == "media":
                cc.send(value)

    last_pressed = pressed
    time.sleep(0.05)
