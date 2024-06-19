import os
import sys
import subprocess
def install_packages():
    packages = ['yt_dlp', 'opencv-python', 'pillow', 'numpy']
    for package in packages:
        try:
            __import__(package)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
install_packages()
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
from yt_dlp import YoutubeDL
def get_youtube_stream(youtube_url):
    ydl_opts = {
        'format': 'best',
        'quiet': True
    }
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=False)
        video_url = info_dict.get('url', None)
    return video_url
class VideoPlayer:
    def __init__(self, root, video_url):
        self.root = root
        self.video_url = video_url
        self.canvas = tk.Canvas(root)
        self.canvas.pack()
        self.vid = cv2.VideoCapture(video_url)
        self.delay = 15
        self.update()
        self.root.mainloop()
    def update(self):
        ret, frame = self.vid.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            self.photo = ImageTk.PhotoImage(image=img)
            self.canvas.config(width=img.width, height=img.height)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.root.after(self.delay, self.update)
if __name__ == "__main__":
    youtube_url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
    video_url = get_youtube_stream(youtube_url)

    root = tk.Tk()
    player = VideoPlayer(root, video_url)
