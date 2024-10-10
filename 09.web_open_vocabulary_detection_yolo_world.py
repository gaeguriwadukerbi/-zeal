from flask import Flask, render_template_string, Response, request, jsonify
from ultralytics import YOLOWorld
import torch
import cv2
import time

app = Flask(__name__)

# GPU가 사용 가능한지 확인 (GPU가 없으면 CPU 사용)
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f'Using device: {device}')

# YOLOv8 모델 불러오기, 선택한 장치로 로드
model = YOLOWorld('yolov8s-worldv2.pt')
model.to(device)  # 모델을 선택한 장치로 이동

# YOLO 모델이 지원하는 클래스 출력 (디버깅용)
#print("YOLO 모델이 지원하는 클래스 목록:", model.names)

# 글로벌 변수로 탐지할 클래스를 관리 (기본값 설정)
desired_classes = ["CUELAB"]
model.set_classes(desired_classes)  # 초기 필터 설정

def generate_frames():
    cap = cv2.VideoCapture(0)  # 웹캠 비디오 캡처 시작
    if not cap.isOpened():
        print("웹캠을 열 수 없습니다.")
        return

    prev_time = 0  # FPS 계산을 위한 이전 시간 초기화

    while True:
        ret, frame = cap.read()
        if not ret:
            print("프레임을 읽을 수 없습니다.")
            break

        # FPS 계산
        current_time = time.time()
        fps = 1 / (current_time - prev_time) if prev_time != 0 else 0
        prev_time = current_time

        try:
            # YOLO 모델로 예측 수행
            results = model.predict(frame, device=device)  # YOLOv8 모델로 객체 탐지 수행
        except IndexError as e:
            print(f"IndexError 발생: {e}")
            continue  # 오류 발생 시 현재 프레임을 건너뛰고 다음 프레임으로 진행

        # 결과를 시각화하여 프레임에 그리기
        annotated_frame = results[0].plot()

        # FPS를 프레임에 추가
        cv2.putText(annotated_frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # 프레임을 JPEG로 인코딩
        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()  # 웹캠 자원 해제

@app.route('/')
def index():
    # HTML 템플릿을 직접 Python 코드에 포함
    HTML_TEMPLATE = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Real Time Open-Vocabulary Object Detection(YOLO-World)</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f0f5;
                margin: 0;
                padding: 0;
                text-align: center;
            }
            h1 {
                background-color: blue;
                color: white;
                padding: 20px 0;
                margin: 0;
                font-size: 2.5em;
            }
            form {
                margin-top: 20px;
                padding: 20px;
                background-color: white;
                border-radius: 10px;
                display: inline-block;
                box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
            }
            input[type="text"] {
                padding: 10px;
                font-size: 16px;
                border: 2px solid blue;
                border-radius: 5px;
                width: 300px;
                margin-bottom: 20px;
            }
            input[type="submit"] {
                background-color: lightblue;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
            }
            input[type="submit"]:hover {
                background-color: #45a049;
            }
            img {
                margin-top: 20px;
                border: 5px solid #ddd;
                border-radius: 10px;
                box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.2);
            }
            footer {
                margin-top: 40px;
                font-size: 14px;
                color: #555;
            }
        </style>
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <script type="text/javascript">
            $(document).ready(function(){
                $('#detect-form').on('submit', function(event){
                    event.preventDefault();  // 페이지 새로 고침 방지
                    var formData = $(this).serialize();
                    $.ajax({
                        url: '/update_classes',
                        type: 'POST',
                        data: formData,
                        success: function(data) {
                            console.log("Classes updated:", data);
                        },
                        error: function() {
                            console.log("Error updating classes.");
                        }
                    });
                });
            });
        </script>
    </head>
    <body>
        <h1>Real Time Open-Vocabulary Object Detection(YOLO-World)</h1>
        <form id="detect-form">
            <label for="desired_classes">탐지할 객체 입력 (쉼표로 구분):</label><br>
            <input type="text" id="desired_classes" name="desired_classes" placeholder="e.g. person, car, cup" required>
            <br>
            <input type="submit" value="탐지 시작">
        </form>
        <h2>Camera Streaming</h2>
        <img id="video-feed" src="{{ url_for('video_feed') }}" style="width:800px; height:auto;" alt="Camera feed not available">
        <footer>
            <p>&copy; 2024 Real Time Open-Vocabulary Object Detection System by CUELAB. All rights reserved.</p>
        </footer>
    </body>
    </html>
    """
    return render_template_string(HTML_TEMPLATE)


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/update_classes', methods=['POST'])
def update_classes():
    global desired_classes
    # 입력받은 객체 이름을 쉼표로 구분하여 리스트로 처리
    desired_classes_str = request.form.get('desired_classes', '')
    desired_classes = [cls.strip() for cls in desired_classes_str.split(',') if cls.strip()]

    # YOLOWorld 모델의 클래스 필터 업데이트
    model.set_classes(desired_classes)
    
    print(f"Updated desired_classes: {desired_classes}")  # 디버깅을 위한 출력

    return jsonify({'status': 'success', 'classes': desired_classes})


if __name__ == '__main__':
    app.run(debug=True)
