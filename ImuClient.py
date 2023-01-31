import socket
import time

IP_ADDRESS = '127.0.0.1'
PORT_CLIENT = 7010
PORT_SERVER = 7011
BUFFER_SIZE = 2048

class ImuClient:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # IP Adress とPortの指定と割り当て
        self.s.bind((IP_ADDRESS, PORT_CLIENT))

    @property
    def data(self):
        self.s.sendto('hoge'.encode(), (IP_ADDRESS, PORT_SERVER))
        rcv_data, _ = self.s.recvfrom(BUFFER_SIZE)
        d = [float(i) for i in rcv_data.decode().split(', ')]
        acc = [i/4096.0 for i in d[:3]]
        omega = [i/16.4 for i in d[3:]]
        return acc, omega


if __name__ == '__main__':
    imu_client = ImuClient()

    while True:
        time.sleep(0.1)
        print(imu_client.data)
