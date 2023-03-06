import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(14,GPIO.OUT)
GPIO.setup(22,GPIO.IN)
while TRUE:
    GPIO.output(14,GPIO.input(22))

    






