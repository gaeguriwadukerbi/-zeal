import torch
import os
from pathlib import Path
import shutil

# 모델 로드
model = torch.hub.load('ultralytics/yolov5', 'custom', path='C:/Users/AISW-203-116/Documents/1/yolov5/runs/train/exp10/weights/best.pt')

# 이미지 디렉토리 설정
image_dir = 'C:\\Users\\AISW-203-116\\Downloads\\dataset\\val\\images'
helmet_dir = 'C:/Users/AISW-203-116/Downloads/dataset/helmet'
no_helmet_dir = 'C:/Users/AISW-203-116/Downloads/dataset/no_helmet'

# 폴더 생성
os.makedirs(helmet_dir, exist_ok=True)
os.makedirs(no_helmet_dir, exist_ok=True)

# 이미지 파일 확장자 목록
valid_image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.webp']

# 이미지 분류
for img_path in Path(image_dir).rglob('*.*'):
    # 이미지 파일만 처리
    if img_path.suffix.lower() in valid_image_extensions:
        results = model(str(img_path))  # 모델을 통해 이미지 예측
        labels = results.xyxy[0][:, -1].tolist()  # 예측된 클래스 라벨들

        print(f"Image: {img_path}, Labels: {labels}")  # 예측된 클래스 라벨 출력

        if 2.0 in labels:  # 헬멧 미착용 클래스가 있으면
            shutil.copy(img_path, no_helmet_dir)
        elif 1.0 in labels:  # 헬멧 착용 클래스가 있으면
            shutil.copy(img_path, helmet_dir)
        else:
            print(f"Unknown class for image {img_path}, skipping...")
    else:
        print(f"Skipping non-image file: {img_path}")

print("Classification completed!")
