
# FPSAutomaticAiming——基于YOLOV5的FPS类游戏自动瞄准系统
# 声明:
- 本项目仅限于学习交流不可商用，不可用于非法用途。
- 使用本项目产生的任何后果与本人无关。
- 使用本项目则默认同意本声明。
- 鉴于个人科研学习任务繁重，本项目已经不再维护！2023/3/7
# 简介
 -  本项目基于yolov5,实现了一款FPS类游戏的自动瞄准系统。本项目旨在使用现有目标网络结构实现一个完整的落地项目，仅供人工智能及自动控制等方面的学习研究，不可用于非法用途！！！

# 使用方法
  > 1.训练模型。  
  > - 本项目的训练方法请查看[yolov5](https://github.com/ultralytics/yolov5)相关文档。

  > 2.使用。
  > - 启动前在```utils/FPSUtils.py```文件中修改屏幕分辨率，检测框范围等参数。
  > - 请在```FPSdetect.py```文件中修改模型位置:```model = attempt_load('此处改为自己的路径\FPSAutomaticAiming\yolov5s.pt', map_location=device)  # load FP32 model```。
  > - 在```Main.py```中修改鼠标移动的相关代码为自己的鼠标移动代码。
  > - 修改好相关参数后直接运行```Main.py```启动本项目。


# 环境配置
1.软件环境  
  使用conda导入```yolo.yaml```。
2.硬件环境  
  英伟达10系显卡（显存4G+）、最新版显卡驱动
