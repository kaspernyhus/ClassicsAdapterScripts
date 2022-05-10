import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack
import ctypes


def twos_complement(hexstr, bits):
    value = int(hexstr, 16)
    if value & (1 << (bits-1)):
        value -= 1 << bits
    return value


def int2hex(number, bits):
    """ Return the 2'complement hexadecimal representation of a number """
    if number < 0:
        return '0x'+hex((1 << bits) + number)[2:].zfill(8)
    else:
        return '0x'+hex(number)[2:].zfill(8)


def print_samples(samples, bits):
    p_str = ""
    line = 0
    print("-------------------------------------------------------")
    for sample in samples:
        p_str += str(int2hex(sample, bits)) + ","
        line += 1
        if line == 8:
            print(p_str)
            line = 0
            p_str = ""
    print(p_str)
    print("-------------------------------------------------------")


def offset_LUT(samples):
    offset = samples[0]
    new_samples = [sample-offset for sample in samples]
    return new_samples


samples = [
    0x8000, 0xc533, 0xf46e, 0xfeb1, 0xe0bc, 0xa40f, 0x5bf0, 0x1f43,
    0x14e, 0xb91, 0x3acc, 0x8000,
]

bits_per_sample = 16
offset_samples = offset_LUT(samples)
print_samples(offset_samples, bits_per_sample)
print("offset", offset_samples)
fs = 48000
T = 1/fs
N = len(samples)
offset_samples = [ctypes.c_int16(h).value for h in samples]


periods = 1
x_plt = np.arange(0, periods*N)
samples_plt = np.tile(offset_samples, periods)
print(offset_samples)

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
