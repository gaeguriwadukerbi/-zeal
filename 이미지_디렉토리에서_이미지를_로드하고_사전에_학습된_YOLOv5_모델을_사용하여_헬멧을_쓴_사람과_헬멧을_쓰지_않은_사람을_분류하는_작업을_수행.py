# 필요한 모듈 임포트
import torch  # PyTorch 라이브러리. 여기서는 torch.hub를 사용하여 YOLOv5 모델을 로드합니다.
import os  # 운영체제와 상호작용하기 위한 모듈. 디렉토리 생성 등에 사용됩니다.
from pathlib import Path  # 파일 경로를 다루기 위한 모듈. 디렉토리 내 파일을 순회하는 데 사용됩니다.
import shutil  # 파일 복사를 위한 모듈.

# 모델 로드
# 사전에 학습된 YOLOv5 모델을 로드합니다. 'custom' 모델을 사용하며, 'best.pt' 파일을 로드합니다.
model = torch.hub.load('ultralytics/yolov5', 'custom', path='yourpath/to/best.pt')

# 이미지 디렉토리 설정
# 분류할 이미지가 있는 디렉토리 경로입니다.
image_dir = 'yourpath/to/val/images'
# 헬멧을 쓴 사람의 이미지를 저장할 디렉토리 경로입니다.
helmet_dir = 'yourpath/to/helmet'
# 헬멧을 쓰지 않은 사람의 이미지를 저장할 디렉토리 경로입니다.
no_helmet_dir = 'yourpath/to/no_helmet'

# 폴더 생성
# 헬멧을 쓴 사람과 헬멧을 쓰지 않은 사람의 이미지를 저장할 디렉토리를 생성합니다.
# 이미 디렉토리가 존재하는 경우에도 에러 없이 넘어갑니다.
os.makedirs(helmet_dir, exist_ok=True)
os.makedirs(no_helmet_dir, exist_ok=True)

# 유효한 이미지 파일 확장자 목록
# 처리할 이미지 파일의 확장자 목록을 정의합니다.
valid_image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.webp']

# 이미지 분류
# image_dir 디렉토리 내 모든 파일을 순회합니다.
for img_path in Path(image_dir).rglob('*.*'):
    # 이미지 파일만 처리
    if img_path.suffix.lower() in valid_image_extensions:
        # 각 이미지 파일을 모델에 입력하여 예측
        results = model(str(img_path))
        # 예측된 클래스 라벨들을 추출
        labels = results.xyxy[0][:, -1].tolist()

        # 예측된 클래스 라벨 출력
        print(f"Image: {img_path}, Labels: {labels}")

        # 예측된 클래스 라벨에 따라 이미지를 적절한 디렉토리로 복사
        if 2.0 in labels:  # 헬멧 미착용 클래스가 있으면
            shutil.copy(img_path, no_helmet_dir)
        elif 1.0 in labels:  # 헬멧 착용 클래스가 있으면
            shutil.copy(img_path, helmet_dir)
        else:
            # 알려지지 않은 클래스가 있을 경우
            print(f"Unknown class for image {img_path}, skipping...")
    else:
        # 유효하지 않은 파일 확장자를 가진 파일을 건너뜁니다.
        print(f"Skipping non-image file: {img_path}")

# 모든 이미지에 대한 분류 작업이 완료되면 메시지 출력
print("Classification completed!")
