import socket
import netifaces as ni
from parse_log_data import parse_log_data

# Port
port = 3333

# UDP setup for listening
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', port))

print("UDP client starting")
ip = ni.ifaddresses('en0')[ni.AF_INET][0]['addr']
print("This computer:", ip, ":", port)

while 1:
    data_raw, addr = sock.recvfrom(1024)
    # print(data_raw)
    if data_raw:
        # print("--------------------------------------------")
        # print("Received data from:", addr[0], ":", addr[1])
        # print("--------------------------------------------")

        print(parse_log_data(data_raw))


