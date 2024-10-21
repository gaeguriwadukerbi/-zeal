# YOLOv8 라이브러리 및 torch 임포트
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
from ultralytics import YOLO
import torch
import cv2

# GPU가 사용 가능한지 확인 (GPU가 없으면 CPU 사용)
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f'Using device: {device}')

# YOLOv8 모델 불러오기 (선택한 장치를 사용)
model = YOLO('yolov8n.pt').to(device)  # 모델을 지정한 장치로 이동

# 웹캠 비디오 캡처 시작 (기본 카메라)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("웹캠을 열 수 없습니다.")
    exit()

# 실시간 웹캠 객체 탐지
while True:
    # 웹캠 프레임 읽기
    ret, frame = cap.read()
    if not ret:
        print("프레임을 읽을 수 없습니다. 종료합니다.")
        break

    # YOLOv8 모델을 사용하여 프레임에서 객체 탐지
    results = model(frame)

    # 결과를 시각화하여 프레임에 그리기
    annotated_frame = results[0].plot()

    # 화면에 출력
    cv2.imshow("YOLOv8 Real-Time Object Detection", annotated_frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 모든 리소스 해제
cap.release()
cv2.destroyAllWindows()
