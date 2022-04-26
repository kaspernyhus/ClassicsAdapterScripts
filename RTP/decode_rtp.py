

def decode_rtp():
    with open('rtp_dump.txt', 'r') as file:
        lines = file.readlines()
    data_str = [line.strip() for line in lines]
    data_joined = ''.join(data_str)
    rtp_header = data_joined[0:24]

    print("RTP header raw:", rtp_header)

    version = int(rtp_header[0:2], 16) >> 6
    padding = (int(rtp_header[0:2], 16) >> 5) & 0x01
    extension = (int(rtp_header[0:2], 16) >> 4) & 0x01
    csrc = int(rtp_header[0:2], 16) & 0x0F
    marker = (int(rtp_header[2:4], 16) >> 7) & 0x01
    payload_type = int(rtp_header[2:4], 16) & 0x7F
    seq_num = int(rtp_header[4:8], 16)
    timestamp = int(rtp_header[8:16], 16)
    ssrc = int(rtp_header[16:24], 16)

    payload = data_joined[24:32]

    print("------------------------------------------")
    print("RTP HEADER")
    print("------------------------------------------")
    print("Version:\t\t", version)
    print("Padding:\t\t", padding)
    print("Extension\t\t", extension)
    print("CSRC:\t\t\t", csrc)
    print("Marker:\t\t\t", marker)
    print("Payload type:\t", payload_type)
    print("Seq num:\t\t", seq_num)
    print("Timestamp:\t\t", timestamp)
    print("SSRC:\t\t\t", ssrc)
    print("----")
    print("payload:", payload, "...")


decode_rtp()
