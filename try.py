import torch
import os
from pathlib import Path
import shutil

# 모델 로드
model = torch.hub.load('ultralytics/yolov5', 'custom', path='C:/Users/AISW-203-116/Documents/1/yolov5/runs/train/exp/weights/best.pt')

# 이미지 디렉토리 설정
image_dir = 'C:/Users/AISW-203-116/Downloads/dataset/drive/images'
helmet_dir = 'C:/Users/AISW-203-116/Downloads/dataset/helmet'
no_helmet_dir = 'C:/Users/AISW-203-116/Downloads/dataset/no_helmet'

# 폴더 생성
os.makedirs(helmet_dir, exist_ok=True)
os.makedirs(no_helmet_dir, exist_ok=True)

# 이미지 분류
for img_path in Path(image_dir).rglob('*.*'):  # 모든 이미지 파일 형식 사용
    results = model(img_path)  # 모델을 통해 이미지 예측
    labels = results.xyxy[0][:, -1].tolist()  # 예측된 클래스 라벨들

    if 0 in labels:  # 헬멧 미착용 클래스가 있으면
        shutil.copy(img_path, no_helmet_dir)
    elif 1 in labels:  # 헬멧 착용 클래스가 있으면
        shutil.copy(img_path, helmet_dir)
    else:
        print(f"Unknown class for image {img_path}, skipping...")

print("Classification completed!")
