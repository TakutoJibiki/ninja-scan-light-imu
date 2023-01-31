import matplotlib.pyplot as plt
from ImuClient import ImuClient
import time

if __name__ == '__main__':
    init_time = time.time()
    imu_client = ImuClient()

    plot_x = []
    plot_y = []
    ylim = [2, 15]

    while True:
        (ax, ay, az), (ox, oy, oz) = imu_client.data
        plot_x.append(time.time() - init_time)
        plot_y.append(az)
        if len(plot_x) > 100:
            plot_x.pop(0)
            plot_y.pop(0)
        ylim = (min(ylim[0], plot_y[-1]), max(ylim[1], plot_y[-1]))

        plt.cla()
        plt.clf()
        plt.ylim(ylim)
        plt.plot(plot_x, plot_y, color='tab:blue', label='$a_{z}$')
        plt.legend()
        plt.xlabel('Time [sec]')
        plt.ylabel('Acceleration')
        plt.pause(0.01)
