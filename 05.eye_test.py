from imutils import face_utils
from datetime import datetime
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2
import os
from PIL import Image, ImageFont, ImageDraw
import pygame
import threading
import time
#from class_naver_sms_service import naver_sms_sender

#=================================================================
#초기값 설정
#=================================================================
#실행 경로 설정 
this_program_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(this_program_directory)

video_path = 'driver.mp4'

#=================================================================
#얼굴 감지, 눈동자 감지 처리 
#=================================================================
#face detecor pre trained NN 
detector = dlib.get_frontal_face_detector()

#dlib's facial landmark NN 초기화
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# 오른쪽, 왼쪽 눈 좌표 인덱스 
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
	print("Error: 비디오 파일을 열 수 없습니다.")
	exit()
time.sleep(2.0)

while True:
	#웹캠 영상 읽기
	ret, frame = cap.read()
	if not ret:
		print("비디오가 끝났거나 에러가 발생했습니다.")
		break

	frame = imutils.resize(frame, width=720)
	frame = cv2.flip(frame, 1)

	#입력영상 graysale 처리 
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# 얼굴 Detection 
	rects = detector(gray)	
   
	for rect in rects:
		x, y = rect.left(), rect.top()
		w, h = rect.right() - x, rect.bottom() - y
		
		#print( w, h)
		#얼굴 크기가 110이상일때만 눈동자 Detection
		#if (w > 110 ):
		#얼굴 영역 bounding box 그리기
		cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

		#눈동자 Detection(68 landmarks)
		shape = predictor(gray, rect)
		shape = face_utils.shape_to_np(shape)
		
		#왼쪽 및 오른쪽 눈 좌표를 추출한 다음 좌표를 사용하여 양쪽 눈의 눈 종횡비를 계산
		leftEye = shape[lStart:lEnd]
		rightEye = shape[rStart:rEnd]
		
		#print( ear_avg )
		# 양쪽 눈동자 외각선 찾기
		leftEyeHull = cv2.convexHull(leftEye)
		rightEyeHull = cv2.convexHull(rightEye)

		#양쪽 눈동자 녹색 외각선 그리기
		#cv2.drawContours(frame, [leftEyeHull], 0, (0, 255, 0), 1)
		#cv2.drawContours(frame, [rightEyeHull], 0, (0, 255, 0), 1)

		#양쪽 눈동자 녹색 점 그리기
		cv2.circle(frame, tuple(rightEye[[0,0][0]]), 2, (0,255,0), -1)
		cv2.circle(frame, tuple(rightEye[[1,0][0]]), 2, (0,255,0), -1)
		cv2.circle(frame, tuple(rightEye[[2,0][0]]), 2, (0,0,0), -1)
		cv2.circle(frame, tuple(rightEye[[3,0][0]]), 2, (0,0,0), -1)
		cv2.circle(frame, tuple(rightEye[[4,0][0]]), 2, (0,0,0), -1)
		cv2.circle(frame, tuple(rightEye[[5,0][0]]), 2, (0,0,0), -1)   
		
		cv2.circle(frame, tuple(leftEye[[0,0][0]]), 2, (0,255,0), -1)
		cv2.circle(frame, tuple(leftEye[[1,0][0]]), 2, (0,255,0), -1)
		cv2.circle(frame, tuple(leftEye[[2,0][0]]), 2, (0,0,0), -1)
		cv2.circle(frame, tuple(leftEye[[3,0][0]]), 2, (0,0,0), -1)
		cv2.circle(frame, tuple(leftEye[[4,0][0]]), 2, (0,0,0), -1)
		cv2.circle(frame, tuple(leftEye[[5,0][0]]), 2, (0,0,0), -1)
	
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break

cap.release()
cv2.destroyAllWindows()