import cv2
import matplotlib

from FPSDetect import *
from PID import PID
from utils.FPSUtils import *

import numpy as np
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
vc = cv2.VideoCapture(r'C:\Users\cy\Videos\Captures\1.mp4')
rval, frame = vc.read()
pass
mPid = PID(0, 0, 1, 0)
i = 0
rx = []
px = []
while rval:
    img = frame[TOP:TOP + 640, LEFT:LEFT + 640, :]
    dets = detect(img)
    btc, btp = FindBestCenter(dets)
    if btc:
        rx.append(int(LEFT + btc[0]) - SCREEN_CX)
        mPid.now_val = rx[-1]
        pidX = mPid.pid_cmd()
        px.append(pidX)
    else:
        rx.append(0)
        mPid.now_val = 0
        pidX = mPid.pid_cmd()
        px.append(pidX)
    rval, frame = vc.read()
x = np.arange(0, len(rx))

plt.plot(x, rx)
plt.plot(x, px)
plt.show()
