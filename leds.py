from evdev import *
import time
import RPi.GPIO as GPIO
import cipher
dev = InputDevice('/dev/input/event0')

GPIO.setmode(GPIO.BCM)
port_map = {
    'Q': 12,
    'W': 7,
    'E': 8,
    'R': 25,
    'T': 14,
    'Y': 21,
    'U': 24,
    'I': 20,
    'O': 16,
    'P': 23,
    'L': 18,
    'M': 15,
    'A': 27,
    'S': 4,
    'D': 10,
    'F': 17,
    'G': 9,
    'H': 19,
    'J': 3,
    'K': 2,
    'Z': 11,
    'X': 22,
    'C': 5,
    'V': 6,
    'B': 26,
    'N': 13 
    
    
    
    # TODO
}

for port in port_map.values():
    GPIO.setup(port, GPIO.OUT)

scancodes = {
    # Scancode: ASCIICode
    0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
    10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
    20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
    30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u';',
    40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
    50: u'M', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 100: u'RALT'
}

buffer = []
try:
    while True:
        for event in dev.read_loop():
            if event.type == ecodes.EV_KEY and event.value == 0:
                key = scancodes[event.code]
                if len(key) == 1 and 'A' <= key <= 'Z':
                    cipher.move_rotors()
                    print(cipher.encrypt(key))
                    port_num = port_map[cipher.encrypt(key)]
                    GPIO.output(port_num, GPIO.HIGH)
                    time.sleep(1)
                    GPIO.output(port_num, GPIO.LOW)
                    buffer = []
                elif len(key) == 1 and '0' <= key <= '9':
                    buffer.append(int(key))
                elif key == u'CRLF':
                    settings = list(map(lambda x: x[0]*10+x[1],
                                   zip(buffer[::2],buffer[1::2])))
                    cipher.set_indices(*settings)
                    print(settings)
                    buffer = []
                elif key == u'TAB':
                    print("Testing LEDs")
                    keyboard ="QWERTYUIOPLMASDFGHJKZXCVBN"
                    for c in keyboard:
                        print(c)
                        GPIO.output(port_map[c],GPIO.HIGH)
                        time.sleep(0.5)
                        GPIO.output(port_map[c],GPIO.LOW)
                        time.sleep(0.5)
finally:
    for port in port_map.values():
        GPIO.output(port, GPIO.LOW)
    GPIO.cleanup()
