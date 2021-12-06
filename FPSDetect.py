import numpy as np
import torch
from models.experimental import attempt_load
from utils.datasets import letterbox
from utils.general import check_img_size, non_max_suppression, scale_coords, xyxy2xywh
import warnings

warnings.filterwarnings("ignore")
# 选择设备
device = torch.device('cuda')  # 'cuda' if torch.cuda.is_available() else 'cpu')
half = device.type != 'cpu'
# Load model
model = attempt_load('E:\Code\FPSAutomaticAiming\yolov5s.pt', map_location=device)  # load FP32 model
stride = int(model.stride.max())  # model stride
img_size = check_img_size(640, s=stride)  # check img_size
if half:
    model.half()  # to FP16
model.eval()
# Get names and colors
names = model.module.names if hasattr(model, 'module') else model.names
# Run inference
if device.type != 'cpu':
    model(torch.zeros(1, 3, img_size, img_size).to(device).type_as(
        next(model.parameters())))  # run once


def detect(img0):
    """
    :param img0: 要检测的图像
    :return: {'class': cls（目标类型）, 'conf': conf（置信分数）, 'position': xywh（目标屏幕坐标）}
    """
    with torch.no_grad():
        # Padded resize
        img = letterbox(img0, img_size, stride=stride)[0]
        # Convert
        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
        img = np.ascontiguousarray(img)
        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)
        pred = model(img, augment=False)[0]
        # Apply NMS
        pred = non_max_suppression(pred, 0.25, 0.45)
        # Process detections
        detections = []
        for i, det in enumerate(pred):  # detections per image
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], img0.shape).round()
                # Traverse detections
                for *xyxy, conf, cls in reversed(det):
                    xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4))).view(-1).tolist()
                    xywh = [round(x) for x in xywh]
                    xywh = [xywh[0] - xywh[2] // 2, xywh[1] - xywh[3] // 2, xywh[2],
                            xywh[3]]  # 检测到目标位置，格式：（left，top，w，h）
                    cls = names[int(cls)]
                    conf = float(conf)
                    detections.append({'class': cls, 'conf': conf, 'position': xywh})
        return detections
