import os  # 운영체제와 상호작용하기 위한 모듈. 디렉토리 및 파일 처리를 위해 사용합니다.
import cv2  # OpenCV 라이브러리. 이미지 및 비디오 처리를 위해 사용합니다.
import numpy as np  # NumPy 라이브러리. 배열 및 행렬 연산을 위해 사용합니다.
import albumentations as A  # Albumentations 라이브러리. 이미지 증강을 위해 사용합니다.
from PIL import Image  # Pillow 라이브러리. 이미지를 읽고 쓰기 위해 사용합니다.
import unicodedata  # Unicode 데이터베이스. 파일 이름을 ASCII로 변환하기 위해 사용합니다.
import matplotlib.pyplot as plt  # Matplotlib 라이브러리. 이미지를 시각화하기 위해 사용합니다.

# 데이터셋 경로 설정
image_dir = r'yourpath/to/images'  # 이미지 파일들이 위치한 디렉토리 경로입니다.
label_dir = r'yourpath/to/labels'  # 라벨 파일들이 위치한 디렉토리 경로입니다.

# 파일 이름을 ASCII 문자로 변환하는 함수
def convert_to_ascii(filename):
    """
    파일 이름을 ASCII 문자로 변환하는 함수.
    유니코드 문자를 ASCII 문자로 변환합니다.

    Args:
        filename (str): 변환할 파일 이름

    Returns:
        str: 변환된 ASCII 파일 이름
    """
    normalized = unicodedata.normalize('NFKD', filename)  # 유니코드 정규화
    ascii_filename = normalized.encode('ascii', 'ignore').decode('ascii')  # ASCII로 인코딩
    return ascii_filename

# 데이터 증강 함수 정의
def augment_image(image, bboxes, class_labels, transform):
    """
    이미지를 증강하는 함수.
    주어진 변환(transform)을 사용하여 이미지를 증강합니다.

    Args:
        image (numpy.ndarray): 원본 이미지
        bboxes (list): 경계 상자 리스트 (YOLO 형식)
        class_labels (list): 클래스 라벨 리스트
        transform (albumentations.core.composition.Compose): Albumentations 변환 객체

    Returns:
        numpy.ndarray: 증강된 이미지
        list: 증강된 경계 상자 리스트
    """
    transformed = transform(image=image, bboxes=bboxes, class_labels=class_labels)
    return transformed['image'], transformed['bboxes']

# Pillow를 사용하여 이미지를 읽는 함수 정의
def read_image(image_path):
    """
    이미지를 읽어오는 함수.
    Pillow를 사용하여 이미지를 읽고 OpenCV 형식으로 변환합니다.

    Args:
        image_path (str): 이미지 파일 경로

    Returns:
        numpy.ndarray: 읽어온 이미지 배열
    """
    try:
        with Image.open(image_path) as img:
            return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)  # Pillow 이미지를 OpenCV 형식으로 변환
    except Exception as e:
        print(f"Error reading image {image_path}: {e}")
        return None

# 증강된 이미지를 시각화하는 함수
def plot_image_with_bboxes(image, bboxes, title="Image with BBoxes"):
    """
    이미지를 경계 상자와 함께 시각화하는 함수.

    Args:
        image (numpy.ndarray): 이미지 배열
        bboxes (list): 경계 상자 리스트 (YOLO 형식)
        title (str): 이미지 타이틀
    """
    plt.figure(figsize=(10, 10))  # 시각화할 이미지 크기 설정
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))  # BGR 이미지를 RGB로 변환하여 표시
    for bbox in bboxes:  # 각 경계 상자를 순회
        x_center, y_center, width, height = bbox  # 경계 상자 정보 추출
        x1 = int((x_center - width / 2) * image.shape[1])  # 좌측 상단 x 좌표 계산
        y1 = int((y_center - height / 2) * image.shape[0])  # 좌측 상단 y 좌표 계산
        x2 = int((x_center + width / 2) * image.shape[1])  # 우측 하단 x 좌표 계산
        y2 = int((y_center + height / 2) * image.shape[0])  # 우측 하단 y 좌표 계산
        plt.gca().add_patch(plt.Rectangle((x1, y1), x2-x1, y2-y1, fill=False, color='red', linewidth=2))  # 경계 상자 그리기
    plt.title(title)  # 이미지 타이틀 설정
    plt.axis('off')  # 축 숨기기
    plt.show()  # 이미지 표시

# 데이터 증강을 위한 변환 설정
transform = A.Compose([
    A.HorizontalFlip(p=0.5),  # 50% 확률로 좌우 반전
    A.RandomBrightnessContrast(p=0.2),  # 20% 확률로 밝기 및 대비 조정
    A.ShiftScaleRotate(scale_limit=0.1, rotate_limit=10, shift_limit=0.1, p=0.5, border_mode=cv2.BORDER_CONSTANT)  # 이동, 스케일 및 회전 변환
], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels']))  # YOLO 형식의 경계 상자를 사용

# 이미지 디렉토리 내의 모든 파일을 순회
for filename in os.listdir(image_dir):
    if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.webp'):  # 지원하는 이미지 파일 형식 확인
        image_path = os.path.join(image_dir, filename)  # 이미지 파일 경로 설정
        label_path = os.path.join(label_dir, filename.replace('.jpg', '.txt').replace('.png', '.txt').replace('.webp', '.txt'))  # 라벨 파일 경로 설정

        # ASCII 문자로 파일 이름 변환
        try:
            new_filename = convert_to_ascii(filename)  # 파일 이름을 ASCII로 변환
            new_image_path = os.path.join(image_dir, new_filename)  # 새로운 이미지 파일 경로 설정
            new_label_path = os.path.join(label_dir, new_filename.replace('.jpg', '.txt').replace('.png', '.txt').replace('.webp', '.txt'))  # 새로운 라벨 파일 경로 설정

            os.rename(image_path, new_image_path)  # 이미지 파일 이름 변경
            os.rename(label_path, new_label_path)  # 라벨 파일 이름 변경
        except Exception as e:
            print(f"Error renaming files: {e}")  # 파일 이름 변경 중 에러 발생 시 출력
            continue

        # 이미지와 라벨 불러오기
        image = read_image(new_image_path)  # 이미지를 읽어옴
        if image is None:
            print(f"Warning: Unable to read image {new_image_path}. Skipping...")  # 이미지 읽기 실패 시 경고 출력
            continue

        h, w = image.shape[:2]  # 이미지의 높이와 너비 가져오기
        try:
            with open(new_label_path, 'r') as f:  # 라벨 파일 읽기
                bboxes = []  # 경계 상자 리스트 초기화
                class_labels = []  # 클래스 라벨 리스트 초기화
                for line in f.readlines():
                    class_label, x_center, y_center, bbox_width, bbox_height = map(float, line.strip().split())  # 라벨 파일에서 값 읽기
                    bboxes.append([x_center, y_center, bbox_width, bbox_height])  # 경계 상자 추가
                    class_labels.append(class_label)  # 클래스 라벨 추가
        except Exception as e:
            print(f"Error reading label file {new_label_path}: {e}")  # 라벨 파일 읽기 중 에러 발생 시 출력
            continue

        # 증강 횟수 설정
        for i in range(50):  # 각 이미지당 50개의 증강 이미지 생성
            augmented_image, augmented_bboxes = augment_image(image, bboxes, class_labels, transform)  # 이미지 증강

            # 증강된 이미지 저장
            aug_image_path = os.path.join(image_dir, f"{os.path.splitext(new_filename)[0]}_aug_{i}.jpg")  # 증강된 이미지 파일 경로 설정
            cv2.imwrite(aug_image_path, augmented_image)  # 증강된 이미지 저장

            # 증강된 라벨 저장
            aug_label_path = os.path.join(label_dir, f"{os.path.splitext(new_filename)[0]}_aug_{i}.txt")  # 증강된 라벨 파일 경로 설정
            with open(aug_label_path, 'w') as f:  # 증강된 라벨 파일 쓰기 모드로 열기
                for bbox, class_label in zip(augmented_bboxes, class_labels):
                    x_center, y_center, bbox_width, bbox_height = bbox  # 경계 상자 값 가져오기
                    f.write(f"{class_label} {x_center} {y_center} {bbox_width} {bbox_height}\n")  # 라벨 파일에 쓰기

            # 증강된 이미지 시각화 (선택 사항, 필요시 주석 해제)
            # plot_image_with_bboxes(augmented_image, augmented_bboxes, title=f"Augmented {i}")

print("Augmentation complete.")  # 증강 작업 완료 메시지 출력
