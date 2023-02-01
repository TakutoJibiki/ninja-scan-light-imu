import subprocess
import time
import socket
import threading
import Config
from ImuClient import ImuClient

PORT_CLIENT = 6001
PORT_SERVER = 6002
imu_data = ''

def ProcessImu():
    imu_client = ImuClient()
    global imu_data

    while True:
        time.sleep(0.01)
        (ax, ay, az), (ox, oy, oz) = imu_client.data
        imu_data = ','.join(str(i) for i in [ax, ay, az, ox, oy, oz])

if __name__ == '__main__':
    thread = threading.Thread(target=ProcessImu)
    thread.start()

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((Config.IP_ADDRESS, PORT_SERVER))

        print('waiting...')

        while True:
            # クライアントから何かしら送られてくるまで待機
            s.recvfrom(Config.BUFFER_SIZE)

            # IMUのデータを送る
            s.sendto(
                imu_data.encode(),
                (Config.IP_ADDRESS, PORT_CLIENT)
            )
            print(imu_data)
