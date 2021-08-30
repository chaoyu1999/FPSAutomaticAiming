import random
# 初始化yolo网络
import time
from math import *
from decimal import Decimal
from CFDetect import *
from ctypes import *
# 加载相关工具函数
from utils.CFUtils import *
import threading

dll = cdll.LoadLibrary(r'lib/Dll.dll')  # 加载用C语言封装过的“易键鼠”dll
is_screen = False  # 截图标志


class ScreenThread(threading.Thread):
    """
    截图线程,调用截图函数实现全屏截屏
    """

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global is_screen
        while True:
            if is_screen is True:
                screenShot()


def screenShot():
    """
    截取屏幕，提供训练数据
    :return:None
    """
    time.sleep(0.3)
    img = pyautogui.screenshot(region=[0, 0, 1920, 1080])  # region为屏幕截取区域格式为（left，top，w，h）
    img.save('img/' + str(int(time.time())) + '.jpg')


#
#
# def getAngle(x, y):
#     """
#     两向量夹角0~π
#     :param x: 向量1
#     :param y: 向量2
#     :return: angle
#     """
#     result1 = 0.0
#     result2 = 0.0
#     result3 = 0.0
#     for i in range(len(x)):
#         result1 += x[i] * y[i]  # sum(X*Y)
#         result2 += x[i] ** 2  # sum(X*X)
#         result3 += y[i] ** 2  # sum(Y*Y)
#     return acos(result1 / ((result2 * result3) ** 0.5))
#
#
# def CurveTransform(tc, px1):
#     """
#     获得最终坐标系的曲线
#     :param tc: 目标中心
#     :param px1: 坐标系1下的曲线坐标
#     :return: 最终曲线点坐标
#     """
#     if px1 is None:
#         return None, None
#     sc = [SCREEN_CX, SCREEN_CY]
#     lor = 'R'  # tc在屏幕左右标志
#     px2 = [sc]  # 最终曲线点坐标
#     dxy = []
#     v_a = (1, 0)
#     v_b = (tc[1] - sc[1], tc[0] - sc[0])
#     angle = getAngle(v_a, v_b)
#
#     if tc[0] < sc[0]:
#         lor = 'L'
#     if lor == 'R':
#         cos_a = cos(angle)
#         sin_a = sin(angle)
#         # ************************************************此处注意屏幕x,y轴互换****************************
#         for p in px1:
#             x = p[0] * cos_a - p[1] * sin_a + SCREEN_CY
#             y = p[0] * sin_a + p[1] * cos_a + SCREEN_CX
#             dx = x - px2[-1][1]
#             dy = y - px2[-1][0]
#             dxy.append([dx, dy])
#             px2.append([y, x])
#     else:
#         angle = 2 * PI - angle
#         cos_a = cos(angle)
#         sin_a = sin(angle)
#         for p in px1:
#             x = p[0] * cos_a - p[1] * sin_a + SCREEN_CY
#             y = p[0] * sin_a + p[1] * cos_a + SCREEN_CX
#             dx = x - px2[-1][1]
#             dy = y - px2[-1][0]
#             dxy.append([dy, dx])
#             px2.append([y, x])
#     return px2, dxy
#
#
# def GetCurve(tc, sd=15):
#     """
#     获得坐标系1下的坐标点
#     :param sd: 采样距离
#     :param tc: 检测中心
#     :return: 坐标1下曲线点
#     """
#     sc = [SCREEN_CX, SCREEN_CY]
#     d = int(Distence(sc, tc))  # 两点间距离
#     if d >= sd:
#         n = d // sd
#     else:
#         return None
#         # r = d // (2 * PI)  # 参数r
#
#     p = []  # 坐标系1下的曲线点
#     for i in range(1, n + 1):
#         t = d * i / n
#         x = t
#         y = 0
#         p.append([x, y])
#     return p


#
# if __name__ == "__main__":
#     # a = getAngle([0, -1], [-1, 1])
#     # print(a)
#
#     p2, dx2 = CurveTransform([1920, 1080], GetCurve([1920, 1080]))
#     for p in p2:
#         dll.MoveTo2(int(p[0]), int(p[1]))

if __name__ == "__main__":
    """
    运行神经自瞄
    """
    # 启动截图线程收集训练数据
    # st = ScreenThread()
    # st.start()

    while True:
        try:
            img = ScreenShout()  # 截取屏幕检测区域
            detections = detect(img)  # 送入yolo检测
            btc, btp = FindBestCenter(detections)  # 确定目标最优的射击中心
            is_screen = False  # 有目标，截图保存训练数据
            if btc is not None:  # 如果屏幕区域有射击目标
                is_screen = True  # 有目标，截图保存训练数据
                # 对鼠标移动的直线进行采样，防止被封号，采样间隔sd = 10像素
                x = btc[0] - SCREENSHOT_W // 2  # x相对移动距离
                y = btc[1] - SCREENSHOT_H // 2  # y相对移动距离
                sd = 10  # 采样率
                sx = 1 if x >= 0 else -1  # 取x的符号
                sy = 1 if y >= 0 else -1  # 取y的符号
                x = abs(x)
                y = abs(y)
                xn = x // sd  # x采样次数
                xnr = x % sd  # x采样剩余
                yn = y // sd
                ynr = y % sd
                if xn >= yn:
                    for i in range(yn):
                        dll.MoveR2(sx * sd, sy * sd)
                    for i in range(xn - yn):
                        dll.MoveR2(sx * sd, 0)
                    dll.MoveR2(sx * xnr, sy * ynr)
                else:
                    for i in range(xn):
                        dll.MoveR2(sx * sd, sy * sd)
                    for i in range(yn - xn):
                        dll.MoveR2(0, sy * sd)
                    dll.MoveR2(sx * xnr, sy * ynr)
        except:
            print('问题不大')
