import os  # 운영체제와 상호작용하기 위한 모듈. 디렉토리와 파일을 처리하는 데 사용됩니다.
import json  # JSON 파일을 읽고 쓰기 위한 모듈.

# 경로 설정
json_dir = 'yourpath/to/json'  # JSON 파일들이 위치한 디렉토리 경로입니다.
images_dir = 'yourpath/to/images'  # 이미지 파일들이 위치한 디렉토리 경로입니다.
labels_dir = 'yourpath/to/labels'  # 변환된 YOLO 형식의 레이블 파일들이 저장될 디렉토리 경로입니다.

# 라벨 디렉토리가 존재하지 않으면 생성
os.makedirs(labels_dir, exist_ok=True)  # 레이블 파일을 저장할 디렉토리를 생성합니다. 이미 존재하면 아무 작업도 하지 않습니다.

# JSON 파일들 처리
for json_file in os.listdir(json_dir):  # json_dir 디렉토리 내의 모든 파일을 순회합니다.
    if json_file.endswith('.json'):  # 파일이 .json 확장자로 끝나는지 확인합니다.
        json_path = os.path.join(json_dir, json_file)  # JSON 파일의 전체 경로를 생성합니다.

        # JSON 파일 로드 (UTF-8 인코딩으로)
        with open(json_path, encoding='utf-8') as f:  # JSON 파일을 읽기 모드로 열고 데이터를 파싱하여 딕셔너리로 변환합니다.
            data = json.load(f)  # JSON 데이터를 파싱하여 딕셔너리로 변환합니다.

        # 이미지 파일명 가져오기
        image_filename = data['imagePath']  # JSON 데이터에서 이미지 파일명을 추출합니다.
        image_path = os.path.join(images_dir, image_filename)  # 이미지 파일의 전체 경로를 생성합니다.
        
        # 이미지 크기 가져오기
        width = data['imageWidth']  # JSON 데이터에서 이미지의 너비를 추출합니다.
        height = data['imageHeight']  # JSON 데이터에서 이미지의 높이를 추출합니다.

        # 어노테이션을 읽고 라벨 파일 생성
        label_filename = os.path.splitext(image_filename)[0] + '.txt'  # 이미지 파일명을 기반으로 라벨 파일명을 생성합니다.
        label_path = os.path.join(labels_dir, label_filename)  # 라벨 파일의 전체 경로를 생성합니다.
        
        with open(label_path, 'w') as f:  # 라벨 파일을 쓰기 모드로 열고 어노테이션 정보를 작성합니다.
            for shape in data['shapes']:  # JSON 데이터에서 모든 어노테이션(shape)을 순회합니다.
                label = shape['label']  # 어노테이션의 라벨을 추출합니다.
                points = shape['points']  # 어노테이션의 좌표점을 추출합니다.
                
                # 어노테이션이 사각형인 경우
                if shape['shape_type'] == 'rectangle':
                    x_min = min(points[0][0], points[1][0])  # 사각형의 좌측 상단 x 좌표를 계산합니다.
                    y_min = min(points[0][1], points[1][1])  # 사각형의 좌측 상단 y 좌표를 계산합니다.
                    x_max = max(points[0][0], points[1][0])  # 사각형의 우측 하단 x 좌표를 계산합니다.
                    y_max = max(points[0][1], points[1][1])  # 사각형의 우측 하단 y 좌표를 계산합니다.
                # 어노테이션이 다각형인 경우
                elif shape['shape_type'] == 'polygon':
                    x_min = min([p[0] for p in points])  # 다각형의 최소 x 좌표를 계산합니다.
                    y_min = min([p[1] for p in points])  # 다각형의 최소 y 좌표를 계산합니다.
                    x_max = max([p[0] for p in points])  # 다각형의 최대 x 좌표를 계산합니다.
                    y_max = max([p[1] for p in points])  # 다각형의 최대 y 좌표를 계산합니다.
                else:
                    # 지원되지 않는 shape_type인 경우 경고 메시지를 출력하고 다음 어노테이션으로 이동합니다.
                    print(f"Unsupported shape type {shape['shape_type']} in {json_file}")
                    continue
                
                # YOLO 형식으로 변환
                x_center = (x_min + x_max) / 2 / width  # 경계 상자의 중심 x 좌표를 YOLO 형식으로 변환합니다.
                y_center = (y_min + y_max) / 2 / height  # 경계 상자의 중심 y 좌표를 YOLO 형식으로 변환합니다.
                bbox_width = (x_max - x_min) / width  # 경계 상자의 너비를 YOLO 형식으로 변환합니다.
                bbox_height = (y_max - y_min) / height  # 경계 상자의 높이를 YOLO 형식으로 변환합니다.

                # 클래스 ID는 헬멧 착용(0)과 미착용(1)으로 가정합니다. 필요에 따라 수정하세요.
                if label == 'helmet':
                    class_id = 0  # 헬멧 착용 클래스는 0
                elif label == 'no_helmet':
                    class_id = 1  # 헬멧 미착용 클래스는 1
                else:
                    # 알 수 없는 라벨인 경우 경고 메시지를 출력하고 다음 어노테이션으로 이동합니다.
                    print(f"Unknown label {label} in {json_file}, skipping...")
                    continue

                # 변환된 정보를 텍스트 파일로 저장 (YOLO 형식: 클래스 ID, 중심 x, 중심 y, 너비, 높이)
                f.write(f"{class_id} {x_center} {y_center} {bbox_width} {bbox_height}\n")

# 변환 완료 메시지 출력
print("JSON to YOLO label conversion completed.")  # 변환 작업이 완료되었음을 알리는 메시지를 출력합니다.
