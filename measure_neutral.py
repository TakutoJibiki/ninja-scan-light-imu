from ImuClient import ImuClient
import pandas as pd
import numpy as np
import time

if __name__ == '__main__':
    imu_client = ImuClient()

    init_time = time.time()
    datas = []
    while time.time() - init_time < 5.0:
        (ax, ay, az), (ox, oy, oz) = imu_client.data
        datas.append([ax, ay, az, ox, oy, oz])
        print(f'\r{round(time.time() - init_time, 2)} sec', end='')
        time.sleep(0.02)
    print()

    df = pd.DataFrame(datas)
    df.to_csv('acc.csv', header=None, index=None)
    axb, ayb, azb, oxb, oyb, ozb = [np.mean(df.iloc[:, i]) for i in range(6)]
    print(axb, ayb, azb)
    print(oxb, oyb, ozb)
