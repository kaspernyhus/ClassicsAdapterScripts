import matplotlib.pyplot as plt
import numpy as np
from math import ceil, floor
import scipy.fftpack
from PCM_DataPlotting.plotting import plot_fft


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
fs = 48000
fw = 10000.  # wanted freq
N = round(fs/fw)
T = 1/fs
f = fs/N    # real freq


x = np.arange(N)

A = floor((pow(2, bits)-1)/2)
samples = A*np.sin(2.0*np.pi*f*x*T)
samples = [round(sample) for sample in samples]
print(samples)

print("bits:", bits, "fs:", fs, "f:", fw, "f_real:", f, "N:", N, "T:", T, "A:", A)

hex_samples = [int2hex(int(h), bits) for h in samples]
print("LUT length:", len(hex_samples))

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

samples = [twos_complement(h, bits) for h in hex_samples]

periods = 1
x_plt = np.arange(0, periods*N)
samples_plt = np.tile(samples, periods)

plt.figure()
plt.plot(x_plt, samples_plt)
plt.stem(x_plt, samples_plt)

# FFT
# Number of sample points
N = len(samples_plt)
yf = scipy.fftpack.fft(samples_plt)
xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
plt.figure()
plt.plot(xf, 2.0/N * np.abs(yf[:N//2]))
plt.xscale('log')

plt.show()

