import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
dac = [26, 19, 13, 6, 5, 11, 9, 10]
comp = 4
troyka = 17

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def dec2bin(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]


def adc():
    k = 0
    for i in range(7, -1, -1):
        k += 2**i
        GPIO.output(dac, dec2bin(k))
        time.sleep(0.01)
        if GPIO.input(comp) == 0:
            k-= 2**i
    return  k


try:
    while True:
        value = adc()
        if value != 0:
            print('значение dac = {}, напряжение = {:.2f}'.format(value, value*3.3/256))
        #time.sleep(0.1)
except KeyboardInterrupt:
    print('Программа завершила работу')
finally:
    GPIO.output(dac, 0 )
    GPIO.cleanup()