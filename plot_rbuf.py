import matplotlib.pyplot as plt


def twos_complement(hexstr, bits):
    value = int(hexstr, 16)
    if value & (1 << (bits-1)):
        value -= 1 << bits
    return value


def int2hex(number, bits):
    """ Return the 2'complement hexadecimal representation of a number """
    if number < 0:
        return hex((1 << bits) + number)
    else:
        return hex(number)


def decode_raw16(raw_str, stereo=True):
    samples = [twos_complement(raw_str[i+2:i+4]+raw_str[i:i+2], 16) for i in range(0, len(raw_str), 4)]
    if stereo:
        left = samples[::2]
        right = samples[1::2]
        return [left, right]
    else:
        return [samples, [0]]


def decode_raw24(raw_str, stereo=True):
    hex_samples = [raw_str[i:i+8] for i in range(0, len(raw_str), 8)]  # split string into chunks of 8 = 32bit
    samples = [twos_complement(hex_samples[i], 24) for i in range(0, len(hex_samples))]
    if stereo:
        left = samples[::2]
        right = samples[1::2]
        return [left, right]
    else:
        return [samples, [0]]


def decode_BUFFER_HEX_data(bits, TAG="rbuf"):
    with open('rbuf_data.txt', 'r') as file:
        lines = file.readlines()
    split_by = TAG+":"
    # Remove text before 'rbuf:', strip whitespace at start and end and remove spaces between bytes
    data_str = [line.split(split_by)[1].strip().replace(" ", "") for line in lines]

    # Join all data strings into one line
    data_joined = ''.join(data_str)
    if bits == 16:
        samples = decode_raw16(data_joined, bits)
    else:
        samples = decode_raw24(data_joined, bits)
    print("BUFFER_HEX decoded.", "Number of samples:", len(samples[0]+samples[1]))
    return samples


def plot_samples(samples):
    fig, axs = plt.subplots(2, sharex=True)
    fig.suptitle('')
    axs[0].stem(samples[0])
    axs[1].stem(samples[1])
    plt.show()


if __name__ == '__main__':
    data_raw = "56341200"
    decode_raw24(data_raw)