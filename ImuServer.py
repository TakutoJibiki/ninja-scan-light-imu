import subprocess
import time
import socket
import threading
import Config

imu_data = ''

def Imu():
    # 前回起動したプロセスを終了
    subprocess.Popen(
        'taskkill /IM log_CSV.exe /F',
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(1)

    # データ取得開始
    proc = subprocess.Popen(
        'log_CSV.exe COM3 --direct_sylphide=on --page=A',
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

    # 最初の不要なデータを読み出す
    for i in range(4):
        proc.stdout.readline().decode('shift_jis')

    global imu_data
    while True:
        line = proc.stdout.readline().decode('shift_jis').rstrip('\r\n').split(', ')
        imu_data = ', '.join(line[2:8])
        print(imu_data)


if __name__ == '__main__':
    thread = threading.Thread(target=Imu)
    thread.start()

    # 入力データを通信で受け取る
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # IP Adress とPortの指定と割り当て
        s.bind((Config.IP_ADDRESS, Config.PORT_SERVER))

        while True:
            # クライアントから何かしら送られてくるまで待機
            s.recvfrom(Config.BUFFER_SIZE)

            # IMUのデータを送る
            s.sendto(
                imu_data.encode(),
                (Config.IP_ADDRESS, Config.PORT_CLIENT)
            )
