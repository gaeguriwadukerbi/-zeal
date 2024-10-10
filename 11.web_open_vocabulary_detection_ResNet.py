import cv2
import torch
from flask import Flask, render_template_string, Response, request
from transformers import DetrImageProcessor, DetrForObjectDetection
import atexit
import time

app = Flask(__name__)

# Load pretrained DETR model and image processor
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50").to(device)

# Start camera capture
cap = cv2.VideoCapture(0)  # Use the default camera

# 글로벌 변수로 탐지할 클래스를 관리
desired_classes_global = []  # 초기값은 빈 리스트

# HTML 템플릿을 문자열로 정의
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Real Time Open-Vocabulary Object Detection(DETR-ResNet-50)</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f5;
            margin: 0;
            padding: 0;
            text-align: center;
        }
        h1 {
            background-color: #4CAF50;
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
            border: 2px solid #4CAF50;
            border-radius: 5px;
            width: 300px;
            margin-bottom: 20px;
        }
        input[type="submit"] {
            background-color: #4CAF50;
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
                event.preventDefault();
                var formData = $(this).serialize();
                $.post('/update_classes', formData, function(data){
                    console.log("Classes updated");
                });
            });
        });
    </script>
</head>
<body>
    <h1>Real Time Open-Vocabulary Object Detection(DETR-ResNet-50)</h1>
    <form id="detect-form">
        <label for="desired_classes">탐지할 객체 입력 (쉼표로 구분):</label><br>
        <input type="text" id="desired_classes" name="desired_classes" placeholder="e.g. person, car, cup" required>
        <br>
        <input type="submit" value="탐지 시작">
    </form>
    <h2>Camera Streaming</h2>
    <img src="{{ url_for('video_feed') }}" style="width:800px; height:auto;">
    <footer>
        <p>&copy; 2024 Real Time Open-Vocabulary Object Detection System by CUELAB. All rights reserved.</p>
    </footer>
</body>
</html>
"""

def generate_frames():
    global desired_classes_global
    prev_time = 0  # 이전 프레임의 시간을 저장하는 변수
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # FPS 계산
        current_time = time.time()  # 현재 시간
        fps = 1 / (current_time - prev_time) if prev_time != 0 else 0  # 이전 시간과 현재 시간의 차이를 이용해 FPS 계산
        prev_time = current_time  # 현재 시간을 이전 시간으로 저장

        # Convert frame from BGR to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Resize the image for the model input
        image_resized = cv2.resize(image, (800, 600))

        # Preprocess the image
        inputs = processor(images=image_resized, return_tensors="pt").to(device)

        # Perform object detection
        with torch.no_grad():
            outputs = model(**inputs)

        # Get logits and bounding boxes
        logits = outputs.logits.squeeze(0)  # Remove batch dimension
        bboxes = outputs.pred_boxes.squeeze(0)

        # Set confidence threshold
        threshold = 0.5
        probas = logits.softmax(-1)
        keep = probas.max(-1).values > threshold

        # Draw bounding boxes for detected classes
        for box, label in zip(bboxes[keep], probas[keep]):
            class_id = label.argmax().item()

            # Only process valid class IDs
            if class_id in model.config.id2label:
                class_name = model.config.id2label[class_id]
                if class_name in desired_classes_global:
                    # Convert bounding box to list
                    box = box.tolist()

                    # Calculate coordinates in original image dimensions
                    x_center, y_center, width_box, height_box = box
                    x_min = int((x_center - width_box / 2) * frame.shape[1])
                    x_max = int((x_center + width_box / 2) * frame.shape[1])
                    y_min = int((y_center - height_box / 2) * frame.shape[0])
                    y_max = int((y_center + height_box / 2) * frame.shape[0])

                    # Draw bounding box and label (Red color: BGR = (0, 0, 255))
                    cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 0, 255), 2)
                    cv2.putText(frame, f"{class_name}: {label.max().item():.2f}", 
                                (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # FPS 텍스트 추가
        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/update_classes', methods=['POST'])
def update_classes():
    global desired_classes_global
    # Update the global desired_classes based on the form input
    desired_classes = request.form.get('desired_classes').split(',')
    desired_classes_global = [cls.strip() for cls in desired_classes if cls.strip() in model.config.id2label.values()]
    return '', 204  # No content response for AJAX

# 카메라 해제 및 애플리케이션 종료 시 자원 정리
@atexit.register
def cleanup():
    cap.release()

if __name__ == '__main__':
    app.run(debug=True)
