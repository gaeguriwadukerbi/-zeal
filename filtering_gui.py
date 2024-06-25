import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps

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
    image = Image.fromarray(image)
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

root = Tk()
root.title("Image Filter Tool")
root.geometry("1000x600")

img = None

canvas_original = Canvas(root, width=400, height=400, bg='white')
canvas_original.grid(row=0, column=0, padx=10, pady=10)

canvas_filtered = Canvas(root, width=400, height=400, bg='white')
canvas_filtered.grid(row=0, column=1, padx=10, pady=10)

button_frame = Frame(root)
button_frame.grid(row=1, column=0, columnspan=2, pady=10)

Button(button_frame, text="Open Image", command=load_image).pack(side=LEFT, padx=5)
Button(button_frame, text="Grayscale", command=lambda: apply_filter("Grayscale")).pack(side=LEFT, padx=5)
Button(button_frame, text="Blur", command=lambda: apply_filter("Blur")).pack(side=LEFT, padx=5)
Button(button_frame, text="Edge Detection", command=lambda: apply_filter("Edge Detection")).pack(side=LEFT, padx=5)

root.mainloop()
