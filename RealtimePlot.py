import matplotlib.pyplot as plt
from ImuClient import ImuClient
import time

if __name__ == '__main__':
    init_time = time.time()
    imu_client = ImuClient()

    plot_x = []
    plot_ax = []
    plot_ay = []
    plot_az = []
    plot_ox = []
    plot_oy = []
    plot_oz = []
    fig = plt.figure()

    while True:
        plt.cla()
        plt.clf()

        (ax, ay, az), (ox, oy, oz) = imu_client.data
        plot_x.append(time.time() - init_time)
        plot_ax.append(ax)
        plot_ay.append(ay)
        plot_az.append(az)
        plot_ox.append(ox)
        plot_oy.append(oy)
        plot_oz.append(oz)
        if len(plot_x) > 100:
            plot_x.pop(0)
            plot_ax.pop(0)
            plot_ay.pop(0)
            plot_az.pop(0)
            plot_ox.pop(0)
            plot_oy.pop(0)
            plot_oz.pop(0)

        
        ax1 = fig.add_subplot(2, 1, 1)
        ax1.set_ylim(-4, 4)
        ax1.plot(plot_x, plot_ax, color='tab:blue', label='$a_{x}$')
        ax1.plot(plot_x, plot_ay, color='tab:orange', label='$a_{y}$')
        ax1.plot(plot_x, plot_az, color='tab:green', label='$a_{z}$')
        ax1.legend(loc='lower left')
        ax1.set_xlabel('Time [sec]')
        ax1.set_ylabel('Acceleration [g]')
        ax1.grid()

        ax2 = fig.add_subplot(2, 1, 2)
        ax2.set_ylim(-500, 500)
        ax2.plot(plot_x, plot_ox, color='tab:blue', label='$\\omega_{x}$')
        ax2.plot(plot_x, plot_oy, color='tab:orange', label='$\\omega_{y}$')
        ax2.plot(plot_x, plot_oz, color='tab:green', label='$\\omega_{z}$')
        ax2.legend(loc='lower left')
        ax2.set_xlabel('Time [sec]')
        ax2.set_ylabel('Angular velocity [deg/sec]')
        ax2.grid()
        
        fig.tight_layout()
        plt.pause(0.01)
