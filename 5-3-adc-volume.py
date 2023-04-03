import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [21, 20, 16, 12, 7, 8, 25, 24]
comp = 4
troyka = 17

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(leds, GPIO.OUT)
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
        a = dec2bin(value)
        value = int(value*4.6//26) - 1
        flag = 0
        for i in range(8):
            if i < value:
                a[7-i] = 1
            else:
                a[7-i] = 0


        #flag = False
        #for i in range(len(a)):
        #    if a[i] == 1:
        #        flag = True
        #    if flag == True:
        #        a[i] = 1
        #print(a)
        GPIO.output(leds, a)
        #GPIO.output(leds, dec2bin(value))

        #time.sleep(0.1)
except KeyboardInterrupt:
    print('Программа завершила работу')
finally:
    GPIO.output(dac, 0 )
    GPIO.output(leds, 0)
    GPIO.cleanup()