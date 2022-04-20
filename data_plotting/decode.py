#
#
#

import csv


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


def decode_raw24(raw_str, stereo=True, shift=False):
    if shift:
        #hex_samples = [raw_str[i+2:i + 8] for i in range(0, len(raw_str), 8)]  # split string into chunks of 8 = 32bit
        hex_samples = [raw_str[i+6:i+8]+raw_str[i+4:i+6]+raw_str[i+2:i+4] for i in range(0, len(raw_str), 8)]  # split string into chunks of 8 = 32bit
        print(hex_samples)
    else:
        hex_samples = [raw_str[i:i+6] for i in range(0, len(raw_str), 6)]  # split string into chunks of 6 = 24bit

    samples = [twos_complement(hex_samples[i], 24) for i in range(0, len(hex_samples))]
    if stereo:
        left = samples[::2]
        right = samples[1::2]
        return [left, right]
    else:
        return [samples, [0]]


def decode_BUFFER_HEX_data(bits, TAG="rbuf", shift=False):
    with open('../data/rbuf_data.txt', 'r') as file:
        lines = file.readlines()
    split_by = TAG+":"
    # Remove text before 'rbuf:', strip whitespace at start and end and remove spaces between bytes
    data_str = [line.split(split_by)[1].strip().replace(" ", "") for line in lines]

    # Join all data strings into one line
    data_joined = ''.join(data_str)
    if bits == 16:
        samples = decode_raw16(data_joined)
    else:
        samples = decode_raw24(data_joined, shift=shift)
    print("BUFFER_HEX decoded.", "Number of samples:", len(samples[0]+samples[1]))
    return samples


def decode_LOGIC_2_dump(bits, shift_right=False):
    with open('../data/data.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)  # skip first line
        samples = []
        for row in csv_reader:
            if shift_right:
                hex_sample = row[4][8:-2]
                samples.append(twos_complement(row[4][8:-2], bits))  # Row4 == data, 0x0000000011223300[8:-2] = 00112233
            else:
                samples.append(twos_complement(row[4][10:], bits))  # Row4 == data, 0x0000000011223344[10:] = 11223344
    left = samples[::2]
    right = samples[1::2]
    print("LOGIC_2 dump decoded.", "Number of samples:", len(samples))
    return [left, right]


def decode_wireshark_dump(bits, stereo=False, shift=False):
    with open('../data/wireshark.txt', 'r') as file:
        lines = file.readlines()
    data_str = lines[0]
    if bits == 16:
        samples = decode_raw16(data_str, stereo=stereo)
    else:
        samples = decode_raw24(data_str, shift)
    print("Wireshark dump decoded.", "Number of samples:", len(samples[0]+samples[1]))
    return samples


def decode_GSTREAMER_dump(bits, stereo=True):
    with open('../data/gstreamer.txt', 'r') as file:
        lines = file.readlines()
    split_by = ":"

    # Remove text before 'rbuf:', strip whitespace at start and end and remove spaces between bytes
    data_str = [line[0:76].split(split_by)[1].strip().replace(" ", "") for line in lines]
    # Join all data strings into one line
    data_joined = ''.join(data_str)
    if bits == 16:
        samples = decode_raw16(data_joined)
    else:
        samples = decode_raw24(data_joined, shift=False)
    print("Gstreamer dump decoded.", "Number of samples:", len(samples[0] + samples[1]))
    return samples
