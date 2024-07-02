import yaml  # YAML 파일을 읽고 쓰기 위한 모듈. 여기서는 data.yaml 파일을 생성하는 데 사용됩니다.

# 데이터셋 경로 설정
# 훈련 데이터셋의 이미지가 저장된 디렉토리 경로입니다.
train_image_dir = 'your/path/to/train/images'
# 검증 데이터셋의 이미지가 저장된 디렉토리 경로입니다.
val_image_dir = 'your/path/to/val/images'

# data.yaml 파일 생성
# YOLOv5 모델 훈련을 위한 설정 파일로, 훈련 및 검증 데이터셋의 경로와 클래스 정보를 포함합니다.
data = {
    'train': train_image_dir,  # 훈련 데이터셋 경로를 설정합니다.
    'val': val_image_dir,  # 검증 데이터셋 경로를 설정합니다.
    'nc': 2,  # 클래스 수를 설정합니다. 여기서는 두 개의 클래스(헬멧 착용 및 미착용)가 있습니다.
    'names': ['helmet', 'no_helmet']  # 클래스 이름 목록을 설정합니다.
}

# data.yaml 파일을 생성하고 데이터를 저장합니다.
# 지정된 경로에 data.yaml 파일을 생성하고, 위에서 설정한 데이터를 YAML 형식으로 저장합니다.
with open('your/path/to/data.yaml', 'w') as outfile:
    # yaml.dump() 함수를 사용하여 data 딕셔너리를 YAML 형식으로 변환하고 파일에 씁니다.
    yaml.dump(data, outfile, default_flow_style=False)

# 파일 생성 완료 메시지 출력
# data.yaml 파일이 성공적으로 생성되었음을 사용자에게 알리기 위해 메시지를 출력합니다.
print("data.yaml 파일 생성 완료")
