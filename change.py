import os
import json

# 경로 설정
json_dir = 'C:/Users/AISW-203-116/Downloads/dataset/json'
images_dir = 'C:/Users/AISW-203-116/Downloads/dataset/train/images'
labels_dir = 'C:/Users/AISW-203-116/Downloads/dataset/train/labels'

# 라벨 디렉토리가 존재하지 않으면 생성
os.makedirs(labels_dir, exist_ok=True)

# JSON 파일들 처리
for json_file in os.listdir(json_dir):
    if json_file.endswith('.json'):
        json_path = os.path.join(json_dir, json_file)

        # JSON 파일 로드 (UTF-8 인코딩으로)
        with open(json_path, encoding='utf-8') as f:
            data = json.load(f)

        # 이미지 파일명 가져오기
        image_filename = data['imagePath']
        image_path = os.path.join(images_dir, image_filename)
        
        # 이미지 크기 가져오기
        width = data['imageWidth']
        height = data['imageHeight']

        # 어노테이션을 읽고 라벨 파일 생성
        label_filename = os.path.splitext(image_filename)[0] + '.txt'
        label_path = os.path.join(labels_dir, label_filename)
        
        with open(label_path, 'w') as f:
            for shape in data['shapes']:
                label = shape['label']
                points = shape['points']
                
                if shape['shape_type'] == 'rectangle':
                    x_min = min(points[0][0], points[1][0])
                    y_min = min(points[0][1], points[1][1])
                    x_max = max(points[0][0], points[1][0])
                    y_max = max(points[0][1], points[1][1])
                elif shape['shape_type'] == 'polygon':
                    x_min = min([p[0] for p in points])
                    y_min = min([p[1] for p in points])
                    x_max = max([p[0] for p in points])
                    y_max = max([p[1] for p in points])
                else:
                    print(f"Unsupported shape type {shape['shape_type']} in {json_file}")
                    continue
                
                x_center = (x_min + x_max) / 2 / width
                y_center = (y_min + y_max) / 2 / height
                bbox_width = (x_max - x_min) / width
                bbox_height = (y_max - y_min) / height

                # 클래스 ID는 헬멧 착용(0)과 미착용(1)로 가정합니다. 필요에 따라 수정하세요.
                if label == 'helmet':
                    class_id = 0
                elif label == 'no_helmet':
                    class_id = 1
                else:
                    print(f"Unknown label {label} in {json_file}, skipping...")
                    continue

                f.write(f"{class_id} {x_center} {y_center} {bbox_width} {bbox_height}\n")

print("JSON to YOLO label conversion completed.")
