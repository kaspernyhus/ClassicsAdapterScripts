from threading import Thread
import os
import serial
import time
import collections
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from parse_log_data import parse_log_data, get_data


class SerialPlotter:
    def __init__(self, serial_port='/dev/ttyUSB0', serial_baud=115200, timeout=4, plot_length=100, number_of_plots=2, log_to_csv=False):
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
        self.log_data = []
        self.log_events = [[] for i in range(number_of_plots)]
        self.plot_titles = ['Remote logging' for i in range(number_of_plots)]
        self.event_tags = ['Event' for i in range(number_of_plots)]
        self.plot_log_ids = set()
        self.plot_intervals = [0.0 for i in range(number_of_plots)]
        self.previous_timers = [0.0 for i in range(number_of_plots)]
        self.max_y_recorded = [0.0 for i in range(number_of_plots)]
        for i in range(number_of_plots):
            # self.log_data['timestamps'].append(collections.deque([0] * plot_length, maxlen=plot_length))
            # self.log_data['data'].append(collections.deque([0] * plot_length, maxlen=plot_length))
            self.log_data.append({'timestamps': [0 for i in range(self.plot_length)], 'data': [0 for i in range(self.plot_length)]})
        # CSV
        self.log_to_csv = log_to_csv
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

    def get_serial_data(self, frame, lines, current_value_text, time_text, ax, plot_number):
        # print("log data:", self.log_data)
        # print("events:", self.log_events)

        # Calculate update interval
        current_time = time.perf_counter()
        self.plot_intervals[plot_number] = int((current_time - self.previous_timers[plot_number]) * 1000)
        self.previous_timers[plot_number] = current_time
        time_text.set_text('update interval = ' + str(self.plot_intervals[plot_number]) + 'ms')

        # Set text
        current_value_text.set_text("current value = " + str(self.log_data[plot_number]['data'][-1]))
        lines.set_data(self.log_data[plot_number]['timestamps'], self.log_data[plot_number]['data'])
        lines.set_label(('label1', 'label2'))
        ax.set_xlim(self.log_data[plot_number]['timestamps'][0], self.log_data[plot_number]['timestamps'][-1])

        # rescale y axis if needed
        latest_y = self.log_data[plot_number]['data'][-1]
        if latest_y > self.max_y_recorded[plot_number]:
            ax.set_ylim(0, latest_y+latest_y*0.1)
            self.max_y_recorded[plot_number] = latest_y

        # plot events lines
        if self.log_events[plot_number]:
            event = self.log_events[plot_number][-1]
            ax.vlines(x=event, ymin=0, ymax=self.max_y_recorded[plot_number]+self.max_y_recorded[plot_number]*0.11, colors='k', ls='--')
            ax.text(event, self.max_y_recorded[plot_number] / 2, self.event_tags[plot_number], rotation=90,
                    verticalalignment='center')
            self.log_events[plot_number].remove(event)  # remove from event list to only draw once

        ax.set_title("Log ID:" + str(plot_number+1) + " " + self.plot_titles[plot_number])

    def background_thread(self):
        # time.sleep(0.1)
        self.serialConnection.reset_input_buffer()

        if self.log_to_csv:
            date = datetime.now().strftime("%y%m%d_%H%M")
            script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
            rel_path = 'LoggingData/LoggingData_' + str(date) + '.csv'
            abs_file_path = os.path.join(script_dir, rel_path)
            self.log_file = abs_file_path
            with open(self.log_file, 'w+') as log_file:
                writer = csv.writer(log_file)
                writer.writerow(['id', 'log_type', 'timestamp', 'data'])

        while self.is_running:
            self.raw_log_data = self.serialConnection.readline()
            # print(self.raw_log_data)
            self.is_receiving = True

            parsed_data = parse_log_data(self.raw_log_data)
            # print(parsed_data)
            if parsed_data:
                if parsed_data['type'] == 'ID':
                    self.plot_titles[parsed_data['id']-1] = parsed_data['data']
                    self.plot_log_ids.add(parsed_data['id'])
                if parsed_data['type'] == 'Data':
                    log_id = parsed_data['id']-1
                    self.log_data[log_id]['timestamps'].append(parsed_data['timestamp'])
                    self.log_data[log_id]['data'].append(parsed_data['data'])
                    # Resize data vectors to plot length
                    self.log_data[log_id]['timestamps'] = self.log_data[log_id]['timestamps'][-self.plot_length:]
                    self.log_data[log_id]['data'] = self.log_data[log_id]['data'][-self.plot_length:]
                if parsed_data['type'] == 'Event':
                    event_id = parsed_data['id']-1
                    event_tag = parsed_data['data']
                    self.event_tags[event_id] = event_tag
                    self.log_events[event_id].append(parsed_data['timestamp'])

                if self.log_to_csv:
                    # Save data to CSV file
                    csv_data = list(parsed_data.values())
                    # print(csv_data)
                    with open(self.log_file, 'a') as log_file:
                        csv_writer = csv.writer(log_file)
                        csv_writer.writerow(csv_data)

    def get_plot_length(self):
        return self.plot_length

    def get_number_of_plots(self):
        return self.number_of_plots

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
    ax.set_title('Title')
    ax.set_xlabel("Time")
    ax.set_ylabel("Bytes")
    return fig, ax

