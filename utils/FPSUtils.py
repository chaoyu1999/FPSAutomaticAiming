import math

import pyautogui

import numpy as np

SCREEN_W = 1920  # 屏幕长
SCREEN_H = 1080  # 屏幕高
SCREEN_CX = SCREEN_W // 2  # 屏幕中心x
SCREEN_CY = SCREEN_H // 2  # 屏幕中心y
SCREEN_C = [SCREEN_CX, SCREEN_CY]  # 屏幕中心坐标
SCREENSHOT_W = 640  # 截图区域长
SCREENSHOT_H = 640  # 截图区域高
LEFT = SCREEN_CX - SCREENSHOT_W // 2  # 检测框左上角x
TOP = SCREEN_CY - SCREENSHOT_H // 2  # 检测框左上角y


def ScreenShout():
    """
    截取游戏中要检测区域的图片
    :return: (h,w,c)
    """
    img = pyautogui.screenshot(region=[LEFT, TOP, SCREENSHOT_W, SCREENSHOT_H])
    return np.array(img)


def Center(p):
    """
    返回中心坐标;
    :param p: [lx,ly,w,h]->[左上x坐标，左上y坐标]
    :return: [x,y]
    """
    return [p[0] + p[2] // 2, p[1] + p[3] // 2]


def Distence(a, b):
    """
    两点间距离
    :param a:a点 (xa,ya)
    :param b: b点(xb,yb)
    :return: sqrt((xa-xb)**2 + (yb-ya)**2)
    """
    return math.sqrt(
        ((a[0] - b[0]) ** 2) + ((a[1] - b[1]) ** 2))


def FindBestCenter(detections):
    """
    根据检测的结果，寻找最佳射击坐标
    :param detections: 检测结果
    :return: 最佳射击坐标
    """
    ch = {'p': [0, 0, 0, 0], 'd': float('inf'), 'c': 0.0}  # 离枪口最近的头 p位置 d距离中心距离 c可信度
    cp = {'p': [0, 0, 0, 0], 'd': float('inf'), 'c': 0.0}  # 最枪口近的身子 p位置 d距离中心距离 c可信度
    for dt in detections:
        """
        遍历检测到的目标，找最近的头和身子
        """
        if dt['conf'] > 0.80:  # 只寻找置信度达到70%的头和身子
            dt_p = dt['position']  # 检测出来的目标位置
            dt_c = Center(dt_p)  # w,h

            # if dt['class'] == 'head':  # 判断是不是最优头
            #     dt_d = Distence(dt_c, SCREEN_C)
            #     if dt_d < ch['d']:
            #         ch['p'] = dt['position']
            #         ch['d'] = dt_d
            #         ch['c'] = dt['conf']
            #         pass

            if dt['class'] == 'person':  # 判断是不是最优身子
                dt_d = Distence(dt_c, SCREEN_C)
                if dt_d < cp['d']:
                    cp['p'] = dt['position']
                    cp['d'] = dt_d
                    cp['c'] = dt['conf']
                    pass

    if cp['d'] < float('inf') or ch['d'] < float('inf'):  # 自动选择瞄准部位
        btp = ch['p'] if ch['c'] > cp['c'] else cp['p']  # best target position
        btc = Center(btp)  # best target center
        return btc, btp
    return None, None
