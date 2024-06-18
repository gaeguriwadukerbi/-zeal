import torch
from pathlib import Path
import os
from shutil import copyfile

# YOLOv5 훈련 스크립트
def train_yolov5(data_yaml, cfg, weights, epochs, batch_size, imgsz, device):
    os.system(f"""
    python yolov5/train.py --data {data_yaml} --cfg {cfg} --weights {weights} --epochs {epochs} --batch-size {batch_size} --imgsz {imgsz} --device {device}
    """)

# 경로 설정
data_yaml = 'C:/Users/AISW-203-116/Downloads/dataset/data.yaml'
cfg = 'yolov5s.yaml'
weights = 'yolov5s.pt'

# 하이퍼파라미터 설정
epochs = 10
batch_size = 16
imgsz = 1024
device = 0  # GPU 장치 번호

# YOLOv5 훈련 시작
train_yolov5(data_yaml, cfg, weights, epochs, batch_size, imgsz, device)
