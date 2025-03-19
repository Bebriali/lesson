import RPi.GPIO as g
import matplotlib.pyplot as plt
import time

#translation from dec to bin 
def dec2bin(value):                                     
    return [int(i) for i in bin(value)[2:].zfill(8)]


#measures the voltage on troyka-module
def adc_old():
    exp = 128
    num = 0
    while (exp > 0):
        num += exp
        g.output(dac, dec2bin(num))
        time.sleep(0.01)
        if g.input(comp) == 1:
            num -= exp
        exp //= 2
    return num

def adc():
    lvl = 0
    for i in range(bits_q - 1, -1, -1):
        lvl += 2 ** i
        g.output(dac, dec2bin(lvl))
        time.sleep(0.01)
        comp_value = g.input(comp)
        if (comp_value == 0):
            lvl -= 2 ** i
    return lvl

#puts number to dac output
def num_to_dac(value):
    to_dac = dec2bin(value)
    g.output(dac, to_dac)
    return to_dac

dac = [6, 12,  5,  0,  1, 7, 11, 8]
led = [9, 10, 22, 27, 17, 4,  3, 2]
comp = 14
troyka = 13
bits_q = len(dac)
level_q = 2 ** bits_q

volt_m = 3.3
 
g.setwarnings(False)
g.setmode(g.BCM)

g.setup(troyka, g.OUT, initial = g.LOW)
g.setup(dac, g.OUT)
g.setup(comp, g.IN)
g.setup(led, g.OUT)

volts_msrs = []
times_msrs = []

try:
    beg_t = time.time()
    value = 0

    g.output(troyka, 1)
    while (value / level_q < 0.97):
        value = adc_old()
        print(" volts = {:3}".format(value/level_q * volt_m), " volts% = {:3}%".format(value/level_q))

        num_to_dac(value)

        volts_msrs.append(value)
        times_msrs.append(time.time() - beg_t)

    g.output(troyka, 0)

    while (value / level_q > 0.02):
        value = adc()
        print(" volts = {:3}".format(value/level_q * volt_m), " volts% = {:3}%".format(value/level_q))
        #print(" volts = {:3}".format(value/level_q * volt_m))

        num_to_dac(value)

        volts_msrs.append(value)
        times_msrs.append(time.time() - beg_t)

    end_t = time.time()

    #writes average frequency of discretization of measured data to file "settings.txt"
    with open("settings.txt", "w") as f:
        f.write(str((end_t - beg_t) / len(volts_msrs)))
        f.write(("/n"))
        f.write(str(volt_m / 256))

    print(end_t - beg_t, "s/n", len(times_msrs) / (end_t - beg_t), "/n", volt_m / 256)
    print("len times_msrs = ", len(times_msrs))

finally:
    g.output(dac, g.LOW)
    g.output(troyka, g.LOW)
    g.cleanup()


volts_msrs_msg = [str(i) for i in volts_msrs]
times_msrs_msg = [str(i) for i in times_msrs]

with open("data.txt", "w") as f:
    for i in range(len(times_msrs_msg)):
        f.write("/n".join([times_msrs_msg[i], volts_msrs_msg[i]]))

plt.plot(times_msrs, volts_msrs)
plt.savefig("graph.png")
plt.show()




