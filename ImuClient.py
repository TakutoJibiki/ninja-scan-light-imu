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


if __name__ == '__main__':
    imu_client = ImuClient()

    while True:
        time.sleep(0.1)
        print(imu_client.data)
