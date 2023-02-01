import socket
import time
import Config


class ImuClient:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((Config.IP_ADDRESS, Config.PORT_CLIENT))

    @property
    def data(self):
        # IMU のデータを読み込む
        self.s.sendto('hoge'.encode(), (Config.IP_ADDRESS, Config.PORT_SERVER))
        rcv_data, _ = self.s.recvfrom(Config.BUFFER_SIZE)
        d = [float(i) for i in rcv_data.decode().split(', ')]
        acc = [i/4096.0 for i in d[:3]]
        omega = [i/16.4 for i in d[3:]]

        # 値のスケールを実際の物理量に合わせる
        for i in range(3):
            acc[i] -= Config.STOP_ACC[i]
            omega[i] -= Config.STOP_OMEGA[i]
            
        return acc, omega


# if __name__ == '__main__':
#     imu_client = ImuClient()

#     while True:
#         time.sleep(0.1)
#         print(imu_client.data)


if __name__ == '__main__':
    import math
    def hypot3(x, y, z):
        return math.sqrt(x**2 + y**2 + z**2)

    imu_client = ImuClient()

    ax0, ay0, az0 = 0, 0, 0
    max_a_norm = 0
    THROW_THRES = 1
    STOP_THRES = 0.5

    while True:
        time.sleep(0.01)
        (ax, ay, az), _ = imu_client.data
        az -= 1

        a_norm = hypot3(ax, ay, az)
        if a_norm > THROW_THRES and ay*az > 0:
            max_a_norm = max(max_a_norm, a_norm)
            if ay < 0 or az < 0:
                ax *= -1
                ay *= -1
                az *= -1
            ax0, ay0, az0 = ax, ay, az
            print(ax0, ay0, az0)
        elif a_norm < STOP_THRES:
            max_a_norm = 0

        # print(round(ax, 2), round(ay, 2), round(az, 2))
