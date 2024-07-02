# 필요한 모듈 임포트
from pathlib import Path  # 파일 경로를 다루기 위한 모듈. 파일의 경로를 쉽게 처리할 수 있게 해줍니다.
import os  # 운영체제와 상호작용하기 위한 모듈. 예를 들어, 명령줄 명령을 실행할 수 있습니다.
from shutil import copyfile  # 파일 복사를 위한 모듈. 파일을 다른 위치로 복사할 때 사용합니다.

# YOLOv5 훈련 스크립트
# 이 함수는 YOLOv5 모델을 훈련시키기 위해 필요한 인자들을 받아서 명령줄 명령을 생성하여 실행합니다.
def train_yolov5(data_yaml, cfg, weights, epochs, batch_size, imgsz, device):
    """
    YOLOv5 모델을 훈련시키기 위한 함수

    인자:
    - data_yaml: 데이터셋 설정 파일 경로 (str). 데이터셋에 대한 정보(클래스, 이미지 경로 등)가 포함되어 있습니다.
    - cfg: YOLOv5 모델 구성 파일 경로 (str). 모델의 구조를 정의하는 설정 파일입니다.
    - weights: 사전 학습된 가중치 파일 경로 (str). 모델 훈련의 시작점으로 사용할 사전 학습된 가중치 파일입니다.
    - epochs: 훈련할 에포크 수 (int). 전체 데이터셋을 몇 번 반복할지 설정합니다.
    - batch_size: 배치 크기 (int). 한 번에 처리할 이미지의 수를 정의합니다.
    - imgsz: 입력 이미지의 크기 (int). 모델에 입력되는 이미지의 크기입니다.
    - device: 훈련에 사용할 GPU 장치 번호 (int). GPU 장치 번호를 지정하여 GPU에서 훈련을 수행할 수 있습니다.
    """
    # os.system을 사용하여 명령줄 명령어를 생성하고 실행
    os.system(f"""
    python yolov5/train.py --data {data_yaml} --cfg {cfg} --weights {weights} --epochs {epochs} --batch-size {batch_size} --imgsz {imgsz} --device {device}
    """)

# 경로 설정
# 데이터셋 설정 파일 경로. 데이터셋에 대한 정보(클래스, 이미지 경로 등)가 포함된 파일입니다.
data_yaml = 'your/path/to/data.yaml'
# YOLOv5 모델 구성 파일 경로. 모델의 구조를 정의하는 설정 파일입니다.
cfg = 'your/path/to/yolov5s.yaml'
# 사전 학습된 가중치 파일 경로. 모델 훈련의 시작점으로 사용할 사전 학습된 가중치 파일입니다.
weights = 'your/path/to/yolov5s.pt'

# 하이퍼파라미터 설정
# 훈련할 에포크 수. 전체 데이터셋을 몇 번 반복할지 설정합니다.
epochs = 10
# 배치 크기. 한 번에 처리할 이미지의 수를 정의합니다.
batch_size = 16
# 입력 이미지의 크기. 모델에 입력되는 이미지의 크기입니다.
imgsz = 1024
# 훈련에 사용할 GPU 장치 번호 (0번 GPU 사용). GPU 장치 번호를 지정하여 GPU에서 훈련을 수행할 수 있습니다.
device = 0

# YOLOv5 훈련 시작
# 설정된 인자들을 사용하여 train_yolov5 함수를 호출하여 훈련을 시작
train_yolov5(data_yaml, cfg, weights, epochs, batch_size, imgsz, device)
