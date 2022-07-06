from RemoteLogClass import SerialPlotter, make_figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def plot():
    number_of_plots = 2
    s = SerialPlotter('/dev/ttyUSB1', 9600, number_of_plots=number_of_plots, log_to_csv=True)
    s.start()

    # plotting starts below
    update_interval_ms = 100
    x_limit = (0, 1000000)
    y_limit = (0, 1000000)
    x_limits = [x_limit for i in range(number_of_plots)]
    y_limits = [y_limit for i in range(number_of_plots)]
    anim = []
    for i in range(number_of_plots):
        fig, ax = make_figure(x_limits[i], y_limits[i])
        lines = ax.plot([], [])[0]
        update_rate_text = ax.text(0.50, 0.95, '', transform=ax.transAxes)
        current_value_text = ax.text(0.50, 0.90, '', transform=ax.transAxes)
        anim.append(animation.FuncAnimation(fig, s.get_serial_data, fargs=(lines, current_value_text,
                                                                           update_rate_text, ax, i),
                                                                            interval=update_interval_ms))
    plt.show()
    s.close()


if __name__ == '__main__':
    plot()
