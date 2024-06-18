import os
import cv2
import numpy as np
import albumentations as A
from PIL import Image
import unicodedata

# 데이터셋 경로 설정
image_dir = r'C:\Users\AISW-203-116\Downloads\dataset\train\images'
label_dir = r'C:\Users\AISW-203-116\Downloads\dataset\train\labels'

# 파일 이름을 ASCII 문자로 변환하는 함수
def convert_to_ascii(filename):
    normalized = unicodedata.normalize('NFKD', filename)
    ascii_filename = normalized.encode('ascii', 'ignore').decode('ascii')
    return ascii_filename

# 데이터 증식 함수 정의
def augment_image(image, bboxes, class_labels, transform):
    transformed = transform(image=image, bboxes=bboxes, class_labels=class_labels)
    return transformed['image'], transformed['bboxes']

# Pillow를 사용하여 이미지를 읽는 함수 정의
def read_image(image_path):
    try:
        with Image.open(image_path) as img:
            return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    except Exception as e:
        print(f"Error reading image {image_path}: {e}")
        return None

# 데이터 증식 수행
transform = A.Compose([
    A.HorizontalFlip(p=0.5),
    A.RandomBrightnessContrast(p=0.2),
    A.ShiftScaleRotate(scale_limit=0.1, rotate_limit=10, shift_limit=0.1, p=0.5, border_mode=cv2.BORDER_CONSTANT)
], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels']))

for filename in os.listdir(image_dir):
    if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.webp'):
        image_path = os.path.join(image_dir, filename)
        label_path = os.path.join(label_dir, filename.replace('.jpg', '.txt').replace('.png', '.txt').replace('.webp', '.txt'))

        # ASCII 문자로 파일 이름 변환
        new_filename = convert_to_ascii(filename)
        new_image_path = os.path.join(image_dir, new_filename)
        new_label_path = os.path.join(label_dir, new_filename.replace('.jpg', '.txt').replace('.png', '.txt').replace('.webp', '.txt'))

        os.rename(image_path, new_image_path)
        os.rename(label_path, new_label_path)

        # 이미지와 라벨 불러오기
        image = read_image(new_image_path)
        if image is None:
            print(f"Warning: Unable to read image {new_image_path}. Skipping...")
            continue

        h, w = image.shape[:2]
        with open(new_label_path, 'r') as f:
            bboxes = []
            class_labels = []
            for line in f.readlines():
                class_label, x_center, y_center, bbox_width, bbox_height = map(float, line.strip().split())
                bboxes.append([x_center, y_center, bbox_width, bbox_height])
                class_labels.append(class_label)

        # 증식 횟수 설정
        for i in range(50):
            augmented_image, augmented_bboxes = augment_image(image, bboxes, class_labels, transform)

            # 증식된 이미지 저장
            aug_image_path = os.path.join(image_dir, f"{os.path.splitext(new_filename)[0]}_aug_{i}.jpg")
            cv2.imwrite(aug_image_path, augmented_image)

            # 증식된 라벨 저장
            aug_label_path = os.path.join(label_dir, f"{os.path.splitext(new_filename)[0]}_aug_{i}.txt")
            with open(aug_label_path, 'w') as f:
                for bbox, class_label in zip(augmented_bboxes, class_labels):
                    x_center, y_center, bbox_width, bbox_height = bbox
                    f.write(f"{class_label} {x_center} {y_center} {bbox_width} {bbox_height}\n")

print("Augmentation complete.")
