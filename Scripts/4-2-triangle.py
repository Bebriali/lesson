import RPi.GPIO as g
from time import sleep


def dtob (n):
    s = bin(n)[2:].zfill(8)
    s = [int(i) for i in s]
    return s

dac = [8, 11, 7, 1, 0, 5, 12, 6]

g.setmode(g.BCM)
g.setup(dac, g.OUT)

a = 0
mark = 1

try:
    period = float(input("enter period: "))
    while True:
        for i in range (0, 256):
            str_a = dtob(a)

            g.output(dac, str_a)

        if a == 0: mark = 1
        if a == 255: mark = 0
        if mark == 1:
            a += 1
        else:
            a -= 1
        print(a)
        sleep(period/512)

        
finally:
    g.output(dac, 0)
    g.cleanup()