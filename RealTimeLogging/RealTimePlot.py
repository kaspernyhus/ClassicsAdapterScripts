from threading import Thread
import serial
import time
import collections
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import csv
from datetime import datetime

from parse_log_data import parse_log_data, get_data


class SerialPlotter:
    def __init__(self, serial_port='/dev/ttyUSB0', serial_baud=115200, timeout=4, plot_length=10, number_of_plots=2):
        # Serial
        self.port = serial_port
        self.baud = serial_baud
        self.timeout = timeout
        # Thread
        self.thread = None
        self.is_running = True
        self.is_receiving = False
        # Plot
        self.number_of_plots = number_of_plots
        self.plot_length = plot_length
        self.raw_log_data = bytearray()
        self.log_data = {'timestamps': [], 'data': []}
        self.plot_titles = ['Remote logging' for i in range(number_of_plots)]
        self.plot_log_ids = set()
        self.plot_intervals = [0.0 for i in range(number_of_plots)]
        self.previous_timers = [0.0 for i in range(number_of_plots)]
        self.max_y_recorded = [0.0 for i in range(number_of_plots)]
        for i in range(number_of_plots):
            self.log_data['timestamps'].append(collections.deque([0] * plot_length, maxlen=plot_length))
            self.log_data['data'].append(collections.deque([0] * plot_length, maxlen=plot_length))
        # CSV
        self.log_file = ''

        print('Trying to connect to ' + str(self.port) + ' at ' + str(self.baud) + ' BAUD.')
        try:
            self.serialConnection = serial.Serial(self.port, self.baud, timeout=self.timeout)
            print('Connected to ' + str(self.port) + ' at ' + str(self.baud) + ' BAUD.')
        except:
            print("Failed to connect with " + str(self.port) + ' at ' + str(self.baud) + ' BAUD.')
            exit(0)

    def start(self):
        if self.thread is None:
            self.thread = Thread(target=self.background_thread)
            self.thread.start()
            # Block till we start receiving values
            while not self.is_receiving:
                time.sleep(0.1)

    def get_serial_data(self, frame, lines, current_value_text, line_label, time_text, ax, plot_number):
        current_time = time.perf_counter()
        self.plot_intervals[plot_number] = int((current_time - self.previous_timers[plot_number]) * 1000)
        self.previous_timers[plot_number] = current_time
        time_text.set_text('update interval = ' + str(self.plot_intervals[plot_number]) + 'ms')
        current_value_text.set_text(line_label + ' = ' + str(self.log_data['data'][self.plot_length-1]))
        lines.set_data(self.log_data['timestamps'][plot_number], self.log_data['data'][plot_number])
        ax.set_xlim(self.log_data['timestamps'][plot_number][0], self.log_data['timestamps'][plot_number][self.plot_length-1])
        # rescale y axis if needed
        latest_y = self.log_data['data'][plot_number][-1]
        if latest_y > self.max_y_recorded[plot_number]:
            ax.set_ylim(0, latest_y+latest_y*0.1)
            self.max_y_recorded[plot_number] = latest_y
        ax.set_title("Log ID:" + str(plot_number) + " " + self.plot_titles[plot_number])

    def background_thread(self):
        # time.sleep(0.1)
        self.serialConnection.reset_input_buffer()

        date = datetime.now().strftime("%d%m%y_%H%M")
        self.log_file = 'LoggingData/LoggingData_' + str(date) + '.csv'
        with open(self.log_file, 'w') as log_file:
            writer = csv.writer(log_file)
            writer.writerow(['id', 'log_type', 'timestamp', 'data'])

        while self.is_running:
            self.raw_log_data = self.serialConnection.readline()
            # print(self.rawData)
            self.is_receiving = True

            parsed_data = parse_log_data(self.raw_log_data)
            # print(parsed_data)
            if parsed_data:
                if parsed_data['type'] == 'ID':
                    self.plot_titles[parsed_data['id']-1] = parsed_data['data']
                    self.plot_log_ids.add(parsed_data['id'])
                if parsed_data['type'] == 'Data':
                    self.log_data['timestamps'].append(parsed_data['timestamp'])
                    self.log_data['data'].append(parsed_data['data'])
                if parsed_data['type'] == 'Event':
                    self.plot_log_ids.add(parsed_data['id'])
                    self.plot_titles[parsed_data['id']-1] = parsed_data['data']

                # Save data to CSV file
                with open(self.log_file, 'a') as log_file:
                    log_file.write(parsed_data.items())

    def get_plot_length(self):
        return self.plot_length

    def close(self):
        self.is_running = False
        self.thread.join()
        self.serialConnection.close()
        print('Disconnected...')


def make_figure(x_limit, y_limit):
    xmin, xmax = x_limit
    ymin, ymax = y_limit
    fig = plt.figure()
    ax = plt.axes(ylim=(float(ymin - (ymax - ymin) / 1000), float(ymax + (ymax - ymin) / 1000)))
    return fig, ax


def main():
    number_of_plots = 2
    s = SerialPlotter('/dev/ttyUSB0', 9600, number_of_plots=number_of_plots)
    s.start()

    # plotting starts below
    update_interval_ms = 100
    x_limit = (0, 1000000)
    y_limit = (0, 1000000)
    x_limits = [x_limit for i in range(number_of_plots)]
    y_limits = [y_limit for i in range(number_of_plots)]
    line_label = 'Free heap'
    anim = []
    for i in range(number_of_plots):
        fig, ax = make_figure(x_limits[i], y_limits[i])
        lines = ax.plot([], [])[0]
        update_rate_text = ax.text(0.50, 0.95, '', transform=ax.transAxes)
        current_value_text = ax.text(0.50, 0.90, '', transform=ax.transAxes)
        ax.set_title('Title')
        ax.set_xlabel("Timestamps")
        ax.set_ylabel("kBytes")
        anim.append(animation.FuncAnimation(fig, s.get_serial_data, fargs=(lines, current_value_text, line_label,
                                                                           update_rate_text, ax),
                                            interval=update_interval_ms))
        plt.legend(loc="upper left")

    plt.show()

    s.close()


if __name__ == '__main__':
    main()

