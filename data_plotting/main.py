from decode import decode_BUFFER_HEX_data, decode_LOGIC_2_dump, decode_wireshark_dump, decode_GSTREAMER_dump
from stem_plot import plot_samples
from fft_plot import plot_fft


bits_pr_sample = 16
sample_rate = 48000

samples = decode_BUFFER_HEX_data(bits_pr_sample, TAG="log_buffer", shift=True)
#samples = decode_LOGIC_2_dump(bits_pr_sample, shift_right=True)
#samples = decode_wireshark_dump(bits_pr_sample, stereo=True)
#samples = decode_GSTREAMER_dump(bits_pr_sample, stereo=True)

plot_samples(samples, bits_pr_sample)
plot_fft(samples, sample_rate)
