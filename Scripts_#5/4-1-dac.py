import RPi.GPIO as g

def dtob (n):
    s = bin(n)[2:].zfill(8)
    s = [int(i) for i in s]
    return s

dac = [8, 11, 7, 1, 0, 5, 12, 6]

g.setmode(g.BCM)
g.setup(dac, g.OUT)

try:
    while True:
        print("enter the number: ")
        a = input()
        try:
            a = float(a)
            a = int(a)
            if 0 <= a <= 255:

                str_a = dtob(a)

                g.output(dac, str_a)

                volts = float(a)
                volts *= 3.3/256
                print(type(volts))
                print(f'volts are near {volts:.4} v\n')
            elif a < 0:
                print("number under zero")
            elif a > 255:
                print("number is out of range")
        except Exception:
            for i in range(len(a)):
                if (a[i] > '9' or a[i] < '0') and a[i] != '.':
                    print("error in input")
                    break

finally:
    g.output(dac, 0)
    g.cleanup()