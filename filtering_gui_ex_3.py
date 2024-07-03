import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog, Toplevel
from PIL import Image, ImageTk, ImageOps
import threading

def apply_filter(filter_type):
    global img
    if img is None:
        print("No image loaded.")
        return

    if filter_type == "Grayscale":
        filtered_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif filter_type == "Blur":
        filtered_img = cv2.GaussianBlur(img, (15, 15), 0)
    elif filter_type == "Edge Detection":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        filtered_img = cv2.Canny(gray, 100, 200)
    else:
        filtered_img = img

    display_image(filtered_img, canvas_filtered)

def display_image(image, canvas):
    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    
    image = Image.fromarray(image)
    image.thumbnail((canvas_width, canvas_height), Image.LANCZOS)
    
    img_display = ImageTk.PhotoImage(image)
    canvas.image = img_display
    canvas.create_image(0, 0, anchor=NW, image=img_display)
    canvas.config(scrollregion=canvas.bbox(ALL))

def load_image():
    global img
    file_path = filedialog.askopenfilename()
    if file_path:
        print(f"Loading image from {file_path}")
        try:
            pil_image = Image.open(file_path)
            pil_image = ImageOps.exif_transpose(pil_image)
            img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            display_image(img, canvas_original)
        except Exception as e:
            print(f"Failed to load image from {file_path}: {e}")

def rotate_image():
    global img
    if img is not None:
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        display_image(img, canvas_original)

def crop_image():
    global img, cropping, start_point, end_point, crop_window_open
    if img is not None and not crop_window_open:
        cropping = True
        crop_window_open = True
        start_point, end_point = None, None
        cv2.namedWindow("Crop Image")
        cv2.setMouseCallback("Crop Image", mouse_crop)
        while cropping:
            temp_img = img.copy()
            if start_point and end_point:
                cv2.rectangle(temp_img, start_point, end_point, (0, 255, 0), 2)
            cv2.imshow("Crop Image", temp_img)
            key = cv2.waitKey(1)
            if key == 27 or cv2.getWindowProperty("Crop Image", cv2.WND_PROP_VISIBLE) < 1:
                cropping = False
                break
        if start_point and end_point:
            x1, y1 = start_point
            x2, y2 = end_point
            img = img[y1:y2, x1:x2]
            display_image(img, canvas_original)
        cv2.destroyAllWindows()  # 모든 OpenCV 창을 닫습니다.
        cv2.waitKey(1)  # 이벤트 루프를 한 번 더 처리합니다.
        crop_window_open = False



def mouse_crop(event, x, y, flags, param):
    global start_point, end_point, cropping
    if event == cv2.EVENT_LBUTTONDOWN:
        start_point = (x, y)
        end_point = None
    elif event == cv2.EVENT_MOUSEMOVE:
        if start_point:
            end_point = (x, y)
    elif event == cv2.EVENT_LBUTTONUP:
        end_point = (x, y)
        cropping = False

def adjust_brightness_contrast(brightness=50, contrast=50):
    global img
    if img is not None:
        img_adjusted = cv2.convertScaleAbs(img, alpha=contrast/50, beta=brightness-50)
        display_image(img_adjusted, canvas_original)

def open_adjustments_window():
    global adjustments_window
    if adjustments_window is None or not adjustments_window.winfo_exists():
        adjustments_window = Toplevel(root)
        adjustments_window.title("Adjustments")
        adjustments_window.geometry("300x150")

        Label(adjustments_window, text="밝기:").pack()
        brightness_scale = Scale(adjustments_window, from_=0, to=100, orient=HORIZONTAL, command=lambda val: adjust_brightness_contrast(brightness=int(val), contrast=contrast_scale.get()))
        brightness_scale.set(50)
        brightness_scale.pack()

        Label(adjustments_window, text="대비:").pack()
        contrast_scale = Scale(adjustments_window, from_=0, to=100, orient=HORIZONTAL, command=lambda val: adjust_brightness_contrast(brightness=brightness_scale.get(), contrast=int(val)))
        contrast_scale.set(50)
        contrast_scale.pack()

        adjustments_window.protocol("WM_DELETE_WINDOW", lambda: close_adjustments_window(brightness_scale, contrast_scale))

def close_adjustments_window(brightness_scale=None, contrast_scale=None):
    global adjustments_window
    if adjustments_window is not None:
        if brightness_scale and contrast_scale:
            brightness_scale.set(50)
            contrast_scale.set(50)
        adjustments_window.destroy()
        adjustments_window = None

def close_windows():
    global crop_window_open
    close_adjustments_window()
    cv2.destroyAllWindows()
    cv2.waitKey(1)  # 이벤트 루프를 한 번 더 처리합니다.
    crop_window_open = False

def on_closing():
    close_windows()
    root.destroy()

root = Tk()
root.title("이미지 필터 툴")
root.geometry("1000x600")
root.protocol("WM_DELETE_WINDOW", on_closing)

img = None
cropping = False
start_point, end_point = None, None
adjustments_window = None
crop_window_open = False

canvas_original = Canvas(root, width=400, height=400, bg='white')
canvas_original.grid(row=0, column=0, padx=10, pady=10)

canvas_filtered = Canvas(root, width=400, height=400, bg='white')
canvas_filtered.grid(row=0, column=1, padx=10, pady=10)

button_frame = Frame(root)
button_frame.grid(row=1, column=0, columnspan=2, pady=10)

Button(button_frame, text="이미지 열기", command=load_image).pack(side=LEFT, padx=5)
Button(button_frame, text="흑백 처리", command=lambda: apply_filter("Grayscale")).pack(side=LEFT, padx=5)
Button(button_frame, text="블러 처리", command=lambda: apply_filter("Blur")).pack(side=LEFT, padx=5)
Button(button_frame, text="에지 검출", command=lambda: apply_filter("Edge Detection")).pack(side=LEFT, padx=5)
Button(button_frame, text="회전", command=rotate_image).pack(side=LEFT, padx=5)
Button(button_frame, text="자르기", command=lambda: threading.Thread(target=crop_image).start()).pack(side=LEFT, padx=5)
Button(button_frame, text="밝기/대비 조절", command=open_adjustments_window).pack(side=LEFT, padx=5)

root.mainloop()
