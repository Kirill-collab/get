import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
dac = [10, 9, 11, 5, 6, 13, 19, 26][::-1]
comp = 4
troyka = 17

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def dec2bin(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

def adc():
    for i in range(256):
        a = dec2bin(i)
        GPIO.output(dac, a)
        compvalue = GPIO.input(comp)
        time.sleep(0.005)
        if compvalue == 0:
            return i

try:
    while True:
        value = adc()
        if value != 0:
            print('значение dac = {}, напряжение = {:.2f}'.format(value, value*3.3/256))
        time.sleep(0.1)
except KeyboardInterrupt:
    print('Программа завершила работу')
finally:
    GPIO.output(dac, 0 )
    GPIO.cleanup()