from threading import Thread
import serial
import time
import collections
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import struct
import pandas as pd
from parse_log_data import parse_log_data, get_data


class SerialPlotter:
    def __init__(self, serial_port='/dev/ttyUSB0', serial_baud=115200, timeout=4, plot_length=100, dataNumBytes=4):
        self.port = serial_port
        self.baud = serial_baud
        self.timeout = timeout
        self.plotMaxLength = plot_length
        self.rawData = bytearray()
        self.parsed_data = {}
        self.data = collections.deque([0] * plot_length, maxlen=plot_length)
        self.timestamps = collections.deque([0] * plot_length, maxlen=plot_length)
        self.isRun = True
        self.isReceiving = False
        self.thread = None
        self.plot_title = 'Remote logging'
        self.plot_log_id = 0
        self.plotTimer = 0
        self.previousTimer = 0
        self.max_y_recorded = 1000

        print('Trying to connect to: ' + str(self.port) + ' at ' + str(self.baud) + ' BAUD.')
        try:
            self.serialConnection = serial.Serial(self.port, self.baud, timeout=self.timeout)
            print('Connected to ' + str(self.port) + ' at ' + str(self.baud) + ' BAUD.')
        except:
            print("Failed to connect with " + str(self.port) + ' at ' + str(self.baud) + ' BAUD.')
            exit(0)

    def read_serial_start(self):
        if self.thread is None:
            self.thread = Thread(target=self.background_thread)
            self.thread.start()
            # Block till we start receiving values
            while not self.isReceiving:
                time.sleep(0.1)

    def get_serial_data(self, frame, lines, lineValueText, lineLabel, timeText, ax):
        currentTimer = time.perf_counter()
        self.plotTimer = int((currentTimer - self.previousTimer) * 1000)     # the first reading will be erroneous
        self.previousTimer = currentTimer
        timeText.set_text('Plot Interval = ' + str(self.plotTimer) + 'ms')
        lineValueText.set_text('[' + lineLabel + '] = ' + str(self.data[self.plotMaxLength-1]))
        lines.set_data(self.timestamps, self.data)
        ax.set_xlim(self.timestamps[0], self.timestamps[self.plotMaxLength-1])
        latest_y = self.data[-1]
        if latest_y > self.max_y_recorded:
            ax.set_ylim(0, latest_y+latest_y*0.1)
            self.max_y_recorded = latest_y
        ax.set_title("Log ID:" + str(self.plot_log_id) + " " + self.plot_title)


    def background_thread(self):
        # time.sleep(0.1)
        self.serialConnection.reset_input_buffer()
        while (self.isRun):
            self.rawData = self.serialConnection.readline()
            # print(self.rawData)

            parsed_data = parse_log_data(self.rawData)
            if parsed_data:
                self.parsed_data = parsed_data
                self.isReceiving = True

            if self.parsed_data['type'] == 'Data':
                self.timestamps.append(self.parsed_data['timestamp'])
                self.data.append(self.parsed_data['data'])

            if self.parsed_data['type'] == 'ID':
                self.plot_log_id = self.parsed_data['id']
                self.plot_title = self.parsed_data['data']

                # print(self.timestamps, self.data)


    def get_max_plot_length(self):
        return self.plotMaxLength

    def close(self):
        self.isRun = False
        self.thread.join()
        self.serialConnection.close()
        print('Disconnected...')


def main():
    s = SerialPlotter('/dev/ttyUSB0', 9600)
    s.read_serial_start()

    # plotting starts below
    pltInterval = 100    # Period at which the plot animation updates [ms]
    xmin = 0
    xmax = 1000000
    ymin = 0
    ymax = 1000000
    fig = plt.figure()
    ax = plt.axes(ylim=(float(ymin - (ymax - ymin) / 10), float(ymax + (ymax - ymin) / 10)))
    ax.set_title('Arduino Analog Read')
    ax.set_xlabel("Timestamps")
    ax.set_ylabel("Bytes")

    lineLabel = 'Free heap'
    timeText = ax.text(0.50, 0.95, '', transform=ax.transAxes)
    # lines = ax.plot([], [], label=lineLabel)[0]
    lines = ax.plot([], [])[0]
    lineValueText = ax.text(0.50, 0.90, '', transform=ax.transAxes)
    anim = animation.FuncAnimation(fig, s.get_serial_data, fargs=(lines, lineValueText, lineLabel, timeText, ax),
                                   interval=pltInterval)

    plt.legend(loc="upper left")
    plt.show()

    s.close()


if __name__ == '__main__':
    main()
