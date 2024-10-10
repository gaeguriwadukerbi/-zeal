
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
#카메라 / 파일 읽기
#=================================================================
#cap = cv2.VideoCapture(video_path)
cap = cv2.VideoCapture(0)

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
	#입력영상 graysale 처리 
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
 
	cv2.imshow("Frame", gray)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break

cap.release()
cv2.destroyAllWindows()

