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
	
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break

cap.release()
cv2.destroyAllWindows()