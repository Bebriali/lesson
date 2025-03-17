import RPi.GPIO as GPIO
from time import sleep

def dec2bin(n):
    return [int(i) for i in bin(n)[2:].zfill(8)]

dac = [8, 11, 7, 1, 0, 5, 12, 6]

comp = 14
troyka = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)

GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def adc():
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


try:
    while True:
        i = adc()
        volts = i * 3.3 / 256
        
        if i: 
            print("{:.2f}Volts".format(volts))
            print("digit = ", i)
            i = dec2bin(i)
            print("bin = ", i)
            sleep(0.01)

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()



