import cv2
import torch
import time  # FPS 계산을 위한 모듈 추가
from transformers import DetrImageProcessor, DetrForObjectDetection

# 사전 훈련된 DETR 모델과 이미지 프로세서 로드
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50").to(device)

# 탐지할 객체 목록
desired_classes = ["person", "cup", "eyes"]
class_labels = model.config.id2label

# 카메라 캡처 시작
cap = cv2.VideoCapture(0)  # 기본 카메라 사용

# FPS 계산을 위한 이전 시간 초기화
prev_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # FPS 계산
    current_time = time.time()  # 현재 시간
    fps = 1 / (current_time - prev_time) if prev_time != 0 else 0  # FPS 계산
    prev_time = current_time  # 이전 시간 업데이트

    # OpenCV는 BGR 형식으로 이미지를 가져오므로 RGB로 변환
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 입력 이미지 크기 조정
    height, width, _ = frame.shape
    image_resized = cv2.resize(image, (800, 600))

    # 이미지 전처리
    inputs = processor(images=image_resized, return_tensors="pt").to(device)

    # 객체 탐지 수행
    with torch.no_grad():
        outputs = model(**inputs)

    # logits와 bboxes의 크기 및 값 확인
    logits = outputs.logits
    bboxes = outputs.pred_boxes

    # 신뢰도 임계값 설정
    threshold = 0.5
    keep = logits.softmax(-1).max(-1).values > threshold

    # 결과 표시
    for box, label in zip(bboxes[keep], logits.softmax(-1)[keep]):
        class_id = label.argmax().item()

        # class_id가 유효한 경우에만 처리
        if class_id in class_labels:
            class_name = class_labels[class_id]
            if class_name in desired_classes:
                # bbox 좌표 가져오기
                box = box.tolist()

                # 중심 좌표와 크기 (width, height) 계산
                x_center, y_center, width_box, height_box = box

                # 원래 이미지 크기에 맞게 bbox 좌표 변환
                x_min = int((x_center - width_box / 2) * width)
                x_max = int((x_center + width_box / 2) * width)
                y_min = int((y_center - height_box / 2) * height)
                y_max = int((y_center + height_box / 2) * height)

                # bbox 그리기 (붉은색)
                cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 0, 255), 2)
                cv2.putText(frame, f"{class_name}: {label.max().item():.2f}", 
                            (x_min, y_min - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)

    # FPS 표시 (녹색)
    cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)

    # 결과 화면에 출력
    cv2.imshow("Real Time Open-Vocabulary Object Detection(DETR-ResNet-50)", frame)

    # 'q' 키를 눌러 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 카메라 해제 및 윈도우 종료
cap.release()
cv2.destroyAllWindows()
