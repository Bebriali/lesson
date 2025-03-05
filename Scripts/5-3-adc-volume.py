import RPi.GPIO as GPIO
from time import sleep

def dec2bin(n):
    return [int(i) for i in bin(n)[2:].zfill(8)]

dac = [8, 11, 7, 1, 0, 5, 12, 6]
leds = [2, 3, 4, 17, 27, 22, 10, 9]

comp = 14
troyka = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(leds, GPIO.OUT)

GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def adc():
    exp = 128
    num = 0
    while (exp > 0):
        num += exp
        GPIO.output(dac, dec2bin(num))
        sleep(0.01)
        if GPIO.input(comp)==1:
            num -= exp
        exp //=2
    return num

def abc():
    rang = 0
    for i in range(7, -1, -1):
        rang += 2**i

        dac_value = dec2bin(i)
        GPIO.output(dac, dac_value)
        sleep(0.01)
        comp_value = GPIO.input(comp)


        if not comp_value:
            rang -= 2**i
    return rang

def volume(x):
    x = int(x/256*10)
    a = [0]*8
    for i in range(x - 1):
        a[i] = 1
    return a

try:
    while True:
        i = adc()

        #if i:
        h = volume(i) 
        GPIO.output(leds, h)
        volts = i * 3.3 / 256
        print("{:.2f}Volts".format(volts), h)

        #volts = int(volts)
        #volts = dec2bin(volts)
        #print("volts = ", volts)
        #sleep(0.01)


finally:
    GPIO.output(dac, 0)
    GPIO.output(leds, 0)
    GPIO.cleanup()



