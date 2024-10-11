import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
import streamlit as st
import torch
import cv2
from ultralytics import YOLO
import time
import signal
import sys

# GPU가 사용 가능한지 확인
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f'Using device: {device}')

# YOLOv8 모델 로드
model = YOLO('yolov8x-worldv2.pt')
model.to(device)

# Streamlit 애플리케이션 설정
st.title("중복버튼을 만들어내는 공장")

# 검색할 클래스를 설정하는 입력 상자
selected_classes = st.text_input("검색할 객체 (예: person, cup, head):").split(",")
model.set_classes(selected_classes)

# 웹캠에서 객체 탐지 및 표시
def webcam_object_detection():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("웹캠을 열 수 없습니다.")
        return

    prev_time = 0
    stframe = st.empty()

    while True:
        ret, frame = cap.read()
        if not ret:
            st.warning("프레임을 읽을 수 없습니다. 종료합니다.")
            break

        # FPS 계산
        current_time = time.time()
        fps = 1 / (current_time - prev_time) if prev_time != 0 else 0
        prev_time = current_time

        # 객체 탐지
        results = model.predict(frame, device=device)
        annotated_frame = results[0].plot()

        # FPS를 프레임에 추가
        cv2.putText(annotated_frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # 화면에 출력
        stframe.image(annotated_frame, channels="BGR")

        # 종료 버튼이 눌렸는지 확인
        if st.sidebar.button("웹캠 종료", key="stop_button"):
            break

    cap.release()
    cv2.destroyAllWindows()

# Streamlit 버튼을 사용하여 웹캠 탐지 시작
if st.button("웹캠 시작", key="start_button"):
    try:
        webcam_object_detection()
    except KeyboardInterrupt:
        st.write("웹캠 탐지가 중단되었습니다.")
        sys.exit(0)

# 종료 버튼을 추가하여 전체 애플리케이션 종료
if st.button("앱 종료", key="exit_button"):
    st.write("앱을 종료합니다.")
    os.kill(os.getpid(), signal.SIGTERM)