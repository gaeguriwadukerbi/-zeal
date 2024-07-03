import cv2  # OpenCV 라이브러리를 사용하기 위해 import합니다. 이 라이브러리는 컴퓨터 비전 작업을 쉽게 할 수 있게 해줍니다.
import numpy as np  # NumPy 라이브러리를 사용하기 위해 import합니다. 이 라이브러리는 배열 연산을 효율적으로 처리할 수 있게 해줍니다.
from tkinter import *  # Tkinter 모듈을 사용하여 GUI 애플리케이션을 만들기 위해 import합니다.
from tkinter import filedialog  # Tkinter의 파일 다이얼로그 모듈을 import하여 파일 열기/저장 대화 상자를 사용합니다.
from PIL import Image, ImageTk, ImageOps  # PIL (Pillow) 라이브러리를 사용하여 이미지를 쉽게 다룰 수 있게 합니다.

# 필터를 적용하는 함수입니다.
def apply_filter(filter_type):
    global img  # 전역 변수 img를 사용합니다.
    if img is None:  # img가 None인 경우, 즉 이미지를 로드하지 않은 경우
        print("No image loaded.")  # 오류 메시지를 출력합니다.
        return  # 함수를 종료합니다.
    
    # 각 필터 타입에 따라 다른 필터를 적용합니다.
    if filter_type == "Grayscale":
        filtered_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 이미지를 그레이스케일로 변환합니다.
    elif filter_type == "Blur":
        filtered_img = cv2.GaussianBlur(img, (15, 15), 0)  # 이미지를 Gaussian 블러를 적용하여 흐리게 합니다.
    elif filter_type == "Edge Detection":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 먼저 이미지를 그레이스케일로 변환합니다.
        filtered_img = cv2.Canny(gray, 100, 200)  # Canny 알고리즘을 사용하여 가장자리를 검출합니다.
    else:
        filtered_img = img  # 필터 타입이 명시되지 않은 경우 원본 이미지를 사용합니다.

    display_image(filtered_img, canvas_filtered)  # 필터가 적용된 이미지를 화면에 표시합니다.

# 이미지를 화면에 표시하는 함수입니다.
def display_image(image, canvas):
    if len(image.shape) == 2:  # 이미지가 그레이스케일인 경우
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)  # 그레이스케일 이미지를 RGB 이미지로 변환합니다.
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # BGR 형식을 RGB 형식으로 변환합니다.
    
    canvas_width = canvas.winfo_width()  # 캔버스의 너비를 가져옵니다.
    canvas_height = canvas.winfo_height()  # 캔버스의 높이를 가져옵니다.
    
    image = Image.fromarray(image)  # NumPy 배열을 PIL 이미지로 변환합니다.
    image.thumbnail((canvas_width, canvas_height), Image.Resampling.LANCZOS)  # 이미지 크기를 캔버스 크기에 맞게 조정합니다.
    
    img_display = ImageTk.PhotoImage(image)  # PIL 이미지를 Tkinter에서 사용할 수 있는 이미지로 변환합니다.
    canvas.image = img_display  # 이미지 객체를 캔버스에 저장하여 가비지 컬렉션에 의해 제거되지 않도록 합니다.
    canvas.create_image(0, 0, anchor=NW, image=img_display)  # 캔버스에 이미지를 그립니다.
    canvas.config(scrollregion=canvas.bbox(ALL))  # 스크롤 가능한 영역을 이미지 크기에 맞게 설정합니다.

# 이미지를 파일에서 불러오는 함수입니다.
def load_image():
    global img  # 전역 변수 img를 사용합니다.
    file_path = filedialog.askopenfilename()  # 파일 열기 대화 상자를 열고 선택한 파일의 경로를 가져옵니다.
    if file_path:  # 파일 경로가 존재하는 경우
        print(f"Loading image from {file_path}")  # 파일 경로를 출력합니다.
        try:
            pil_image = Image.open(file_path)  # PIL을 사용하여 이미지를 엽니다.
            pil_image = ImageOps.exif_transpose(pil_image)  # 이미지의 EXIF 데이터를 처리하여 올바른 방향으로 회전시킵니다.
            img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)  # PIL 이미지를 NumPy 배열로 변환하고 BGR 형식으로 변환합니다.
            display_image(img, canvas_original)  # 원본 이미지를 화면에 표시합니다.
        except Exception as e:  # 예외가 발생한 경우
            print(f"Failed to load image from {file_path}: {e}")  # 오류 메시지를 출력합니다.

# Tkinter를 사용한 GUI 설정
root = Tk()  # Tkinter의 루트 윈도우를 생성합니다.
root.title("Image Filter Tool")  # 윈도우의 제목을 설정합니다.
root.geometry("1000x600")  # 윈도우의 크기를 설정합니다.

img = None  # 전역 변수 img를 None으로 초기화합니다.

# 원본 이미지를 표시할 캔버스를 생성합니다.
canvas_original = Canvas(root, width=400, height=400, bg='white')
canvas_original.grid(row=0, column=0, padx=10, pady=10)
# canvas_original: 원본 이미지를 표시할 캔버스를 나타냅니다.
# Canvas: Tkinter에서 캔버스를 생성하는 클래스입니다.
# root: Tkinter의 루트 윈도우입니다.
# width=400: 캔버스의 너비를 400으로 설정합니다.
# height=400: 캔버스의 높이를 400으로 설정합니다.
# bg='white': 캔버스의 배경색을 흰색으로 설정합니다.
# grid(row=0, column=0, padx=10, pady=10): 캔버스를 그리드 레이아웃에서 위치시키고, 주위에 여백을 둡니다.

# 필터가 적용된 이미지를 표시할 캔버스를 생성합니다.
canvas_filtered = Canvas(root, width=400, height=400, bg='white')
canvas_filtered.grid(row=0, column=1, padx=10, pady=10)
# canvas_filtered: 필터가 적용된 이미지를 표시할 캔버스를 나타냅니다.
# Canvas: Tkinter에서 캔버스를 생성하는 클래스입니다.
# root: Tkinter의 루트 윈도우입니다.
# width=400: 캔버스의 너비를 400으로 설정합니다.
# height=400: 캔버스의 높이를 400으로 설정합니다.
# bg='white': 캔버스의 배경색을 흰색으로 설정합니다.
# grid(row=0, column=1, padx=10, pady=10): 캔버스를 그리드 레이아웃에서 위치시키고, 주위에 여백을 둡니다.

# 버튼을 배치할 프레임을 생성합니다.
button_frame = Frame(root)
button_frame.grid(row=1, column=0, columnspan=2, pady=10)
# button_frame: 버튼들을 배치할 프레임을 나타냅니다.
# Frame: Tkinter에서 프레임을 생성하는 클래스입니다.
# root: Tkinter의 루트 윈도우입니다.
# grid(row=1, column=0, columnspan=2, pady=10): 프레임을 그리드 레이아웃에서 위치시키고, 주위에 여백을 둡니다.

# 이미지를 여는 버튼을 생성하고 배치합니다.
Button(button_frame, text="Open Image", command=load_image).pack(side=LEFT, padx=5)
# Button: Tkinter에서 버튼을 생성하는 클래스입니다.
# button_frame: 버튼을 배치할 프레임입니다.
# text="Open Image": 버튼에 표시될 텍스트입니다.
# command=load_image: 버튼이 클릭될 때 호출될 함수입니다.
# pack(side=LEFT, padx=5): 버튼을 왼쪽으로 정렬하고, 주위에 여백을 둡니다.

# 그레이스케일 필터를 적용하는 버튼을 생성하고 배치합니다.
Button(button_frame, text="Grayscale", command=lambda: apply_filter("Grayscale")).pack(side=LEFT, padx=5)
# Button: Tkinter에서 버튼을 생성하는 클래스입니다.
# button_frame: 버튼을 배치할 프레임입니다.
# text="Grayscale": 버튼에 표시될 텍스트입니다.
# command=lambda: apply_filter("Grayscale"): 버튼이 클릭될 때 호출될 함수로, "Grayscale" 필터를 적용합니다.
# pack(side=LEFT, padx=5): 버튼을 왼쪽으로 정렬하고, 주위에 여백을 둡니다.

# 블러 필터를 적용하는 버튼을 생성하고 배치합니다.
Button(button_frame, text="Blur", command=lambda: apply_filter("Blur")).pack(side=LEFT, padx=5)
# Button: Tkinter에서 버튼을 생성하는 클래스입니다.
# button_frame: 버튼을 배치할 프레임입니다.
# text="Blur": 버튼에 표시될 텍스트입니다.
# command=lambda: apply_filter("Blur"): 버튼이 클릭될 때 호출될 함수로, "Blur" 필터를 적용합니다.
# pack(side=LEFT, padx=5): 버튼을 왼쪽으로 정렬하고, 주위에 여백을 둡니다.

# 에지 검출 필터를 적용하는 버튼을 생성하고 배치합니다.
Button(button_frame, text="Edge Detection", command=lambda: apply_filter("Edge Detection")).pack(side=LEFT, padx=5)
# Button: Tkinter에서 버튼을 생성하는 클래스입니다.
# button_frame: 버튼을 배치할 프레임입니다.
# text="Edge Detection": 버튼에 표시될 텍스트입니다.
# command=lambda: apply_filter("Edge Detection"): 버튼이 클릭될 때 호출될 함수로, "Edge Detection" 필터를 적용합니다.
# pack(side=LEFT, padx=5): 버튼을 왼쪽으로 정렬하고, 주위에 여백을 둡니다.

root.mainloop()  # Tkinter 이벤트 루프를 시작하여 GUI를 실행합니다.
# root: Tkinter의 루트 윈도우입니다.
# mainloop(): Tkinter 이벤트 루프를 시작하여 사용자의 이벤트를 기다립니다. 이 함수는 프로그램이 종료될 때까지 계속 실행됩니다.
