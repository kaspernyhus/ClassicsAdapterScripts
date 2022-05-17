from decode import decode_BUFFER_HEX_data, decode_LOGIC_2_dump, decode_wireshark_dump, decode_GSTREAMER_dump
from plotting import plot_samples, plot_fft, show_plots


bits_pr_sample = 24
sample_rate = 48000

samples = decode_BUFFER_HEX_data(bits_pr_sample, TAG="buffer", shift=False, endianess='LE')
#samples = decode_LOGIC_2_dump(bits_pr_sample, shift_right=True)
#samples = decode_wireshark_dump(bits_pr_sample, stereo=True, shift=False, endianess='BE')
#samples = decode_GSTREAMER_dump(bits_pr_sample, stereo=True, endianess='BE')

plot_samples(samples, bits_pr_sample)
plot_fft(samples, sample_rate)
show_plots()

