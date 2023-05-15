import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
dac = [10, 9, 11, 5, 6, 13, 19, 26][::-1]
leds = [24, 25, 8, 7, 12, 16, 20, 21]
comp = 4
troyka = 17

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(leds, GPIO.OUT)

def dec2bin(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

def show(value):
    GPIO.output(dac, dec2bin(value))

def adc():
    k = 0
    for i in range(7, -1, -1):
        k += 2**i
        GPIO.output(dac, dec2bin(k))
        time.sleep(0.001)
        if GPIO.input(comp) == 0:
            k-= 2**i
    return  k
#a = 0
#GPIO.output(dac, dec2bin(a))
values = []
try:
    t0 = time.time()
    GPIO.output(troyka, GPIO.HIGH)
    value = 0
    while value/255 < 0.95:
        value = adc()
        values.append(value*3.3/256)
        print(value)
    GPIO.output(troyka, GPIO.LOW)
    while value/256 > 0.02:
        value = adc()
        values.append(value*3.3/256)
        print(value)
        #GPIO.output(leds, dec2bin(value))
    Time = time.time()-t0
    with open('data.txt', 'w') as f:
        for i in values:
            f.write(str(i)+'\n')
    with open('settings.txt', 'w') as f:
        f.write('Значение частоты дискретизации {}Гц'.format(len(values)/Time)+ '\n')
        f.write('Время эксперимента {}с'.format(Time)+ '\n')
        f.write("Шаг квантования {:.4f}В".format(3.3/256)+ '\n')
    print('Значение частоты дискретизации {}Гц'.format(len(values)/Time))
    print('Время эксперимента {}с'.format(Time))
    print("Период одного эксперимента {}с".format(Time/len(values)))
    print("Шаг квантования {:.4f}В".format(3.3/256))
except KeyboardInterrupt:
    print('Программа прервана вручную')
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()