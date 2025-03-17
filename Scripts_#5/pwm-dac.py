import RPi.GPIO as g


g.setmode(g.BCM)
g.setup(9, g.OUT)

n = 10
led = g.PWM(9, 1000)
led.start(0)

try:
    while True:
        force = int(input())
        led.ChangeDutyCycle(force)
        print(3.3*force/100)
finally:
    led.stop()
    g.output(9, 0)
    g.cleanup()