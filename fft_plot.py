import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack
from plot_rbuf import decode_BUFFER_HEX_data, plot_samples


bits_pr_sample = 24
samples = decode_BUFFER_HEX_data(bits_pr_sample, TAG="log_buffer")


plot_samples(samples)


left_ch = samples[0]
right_ch = samples[1]


# Number of samplepoints
N = len(left_ch)
Fs = 48000
T = 1.0 / Fs


yf_L = scipy.fftpack.fft(left_ch)
yf_R = scipy.fftpack.fft(right_ch)

xf = np.linspace(0.0, 1.0/(2.0*T), N//2)

fig, ax = plt.subplots(2)
ax[0].plot(xf, 2.0/N * np.abs(yf_L[:N//2]))
ax[1].plot(xf, 2.0/N * np.abs(yf_R[:N//2]))
ax[0].set_xscale('log')
ax[1].set_xscale('log')
plt.show()