from evdev import *
import time
import RPi.GPIO as GPIO
dev = InputDevice('/dev/input/event0')

GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.OUT)
GPIO.output(5, GPIO.HIGH)
time.sleep(2)
GPIO.output(5, GPIO.LOW)

try:
    while True:
        for event in dev.read_loop():
            if event.type == ecodes.EV_KEY and event.value == 0:
                print(event.value, event.code)
                GPIO.output(5, GPIO.HIGH)
                time.sleep(0.2)
                GPIO.output(5, GPIO.LOW)
finally:
    GPIO.output(5, GPIO.LOW)
    GPIO.cleanup()