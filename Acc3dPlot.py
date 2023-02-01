import matplotlib.pyplot as plt
from ImuClient import ImuClient
import time
import math

THROW_THRES = 1.5


def hypot3(x, y, z):
    return math.sqrt(x**2 + y**2 + z**2)


if __name__ == '__main__':
    imu_client = ImuClient()

    fig = plt.figure(figsize=(8, 8))
    x, y, z = 0, 0, 0   # 始点(x, y, z)の座標を指定
    u0, v0, w0 = 0, 0, 0
    max_a_norm = 0

    while True:
        plt.cla()
        plt.clf()

        (u, v, w), _ = imu_client.data
        w -= 1

        a_norm = hypot3(u, v, w)
        if hypot3(u, v, w) > THROW_THRES and v > 0 and w > 0:
            max_a_norm = max(max_a_norm, a_norm)
            u0, v0, w0 = u, v, w
            print(u0, v0, w0)
        else:
            max_a_norm = 0

        ax = fig.add_subplot(projection='3d') # 3Dプロットの設定
        ax.quiver(x, y, z, u, v, w, arrow_length_ratio=0.1)
        ax.quiver(x, y, z, u0, v0, w0, arrow_length_ratio=0.1, color='red')
        ax.scatter(x, y, z)

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.set_xlim(-4, 4)
        ax.set_ylim(-4, 4)
        ax.set_zlim(-4, 4)
        plt.pause(0.01)
