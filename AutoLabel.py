import FPSDetect as det

import cv2
import os
import shutil

from utils.FPSUtils import FindBestCenter

images_root_path = 'E:/data/CSGO/images/'
center = []
for root, dirs, files in os.walk(images_root_path):
    for file in files:
        file_path = root + file
        # re_f = file_path.replace('images', 'labels').replace('jpg', 'txt')
        # if not os.path.exists(re_f):
        #     shutil.move(file_path, 'E:/data/CSGO/images/NoTarget/')
        img = cv2.imread(file_path)
        res = det.detect(img)
        btc, btp = FindBestCenter(res)
        if btc is not None:
            center.append(btc[0])
            pass
        else:
            center.append(0)
    #     if len(res) == 0:
    #         shutil.move(file_path, 'E:/data/CSGO/images/NoTarget/')
    #     else:
    #         line = []
    #         with open(file_path.replace('images', 'labels').replace('jpg', 'txt'), 'w+') as f:
    #             for i, item in enumerate(res):
    #                 line.append('0' if item['class'] == 'head' else '1')
    #                 item['position'] = [str(int(e) / 640) for e in item['position']]
    #                 for e in item['position']:
    #                     line.append(e)
    #                 line = ' '.join(line)
    #                 line = line + '\n'
    #                 f.write(line)
    #                 line = []
    # break
