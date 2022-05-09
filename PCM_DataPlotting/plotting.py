import matplotlib.pyplot as plt
import scipy.fftpack
import numpy as np


def plot_samples(samples, bits_per_sample):
    max = pow(2, bits_per_sample) / 2
    fig, axs = plt.subplots(2, sharex=True)
    fig.suptitle('')
    axs[0].stem(samples[0])
    axs[1].stem(samples[1])
    axs[0].set_ylim((max, -max))
    axs[1].set_ylim((max, -max))


def plot_fft(samples, fs=48000):
    # FFT
    left_ch = samples[0]
    right_ch = samples[1]

    # Number of sample points
    N = len(left_ch)
    Fs = fs
    T = 1.0 / Fs

    yf_L = scipy.fftpack.fft(left_ch)
    yf_R = scipy.fftpack.fft(right_ch)

    xf = np.linspace(0.0, 1.0/(2.0*T), N//2)

    fig, ax = plt.subplots(2)
    ax[0].plot(xf, 2.0/N * np.abs(yf_L[:N//2]))
    ax[1].plot(xf, 2.0/N * np.abs(yf_R[:N//2]))
    ax[0].set_xscale('log')
    ax[1].set_xscale('log')


def show_plots():
    plt.show()

