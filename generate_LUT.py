import matplotlib.pyplot as plt
import numpy as np
import struct


def int2hex(number, bits):
    """ Return the 2'complement hexadecimal representation of a number """
    if number < 0:
        return '0x'+hex((1 << bits) + number)[2:].zfill(8)
    else:
        return '0x'+hex(number)[2:].zfill(8)


def twos_complement(hexstr, bits):
    value = int(hexstr, 16)
    if value & (1 << (bits-1)):
        value -= 1 << bits
    return value


bits = 24
N = 48
fs = 48000
f = 1000
T = 1/fs

x = np.linspace(0, N-1)
max = pow(2,bits)/2

samples = max*np.sin(2*np.pi*f*x*T)

print(samples)

hex_samples = [int2hex(int(h),bits) for h in samples]

p_str = ""
line = 0
print("-------------------------------------------------------")
for hex_sample in hex_samples:
    p_str += hex_sample + ","
    line += 1
    if line == 8:
        print(p_str)
        line = 0
        p_str = ""
print(p_str)
print("-------------------------------------------------------")


p_str = "I (1008) log_buffer: "
line = 0
print("-------------------------------------------------------")
for hex_sample in hex_samples:
    p_str += hex_sample[2:]
    line += 1
    if line == 4:
        print(p_str)
        line = 0
        p_str = "I (1008) log_buffer: "
print(p_str)
print("-------------------------------------------------------")

p_str = "I (1008) log_buffer: "
line = 0
print("----------------------STEREO---------------------------------")
for hex_sample in hex_samples:
    p_str += hex_sample[2:] + hex_sample[2:]
    line += 1
    if line == 2:
        print(p_str)
        line = 0
        p_str = "I (1008) log_buffer: "
print(p_str)
print("-------------------------------------------------------")

samples = [twos_complement(h,bits) for h in hex_samples]

plt.figure()
plt.plot(x,samples)
plt.show()

