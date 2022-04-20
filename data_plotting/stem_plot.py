import matplotlib.pyplot as plt


def plot_samples(samples, bits_per_sample):
    max = pow(2, bits_per_sample) / 2
    fig, axs = plt.subplots(2, sharex=True)
    fig.suptitle('')
    axs[0].stem(samples[0])
    axs[1].stem(samples[1])
    axs[0].set_ylim((max, -max))
    axs[1].set_ylim((max, -max))
    plt.show()
