import yaml

# 데이터셋 경로 설정
train_image_dir = 'C:/Users/AISW-203-116/Downloads/dataset/train/images'
val_image_dir = 'C:/Users/AISW-203-116/Downloads/dataset/val/images'

# data.yaml 파일 생성
data = {
    'train': train_image_dir,
    'val': val_image_dir,
    'nc': 2,  # 클래스 수
    'names': ['helmet', 'no_helmet']  # 클래스 이름
}

with open('C:/Users/AISW-203-116/Downloads/dataset/data.yaml', 'w') as outfile:
    yaml.dump(data, outfile, default_flow_style=False)

print("data.yaml 파일 생성 완료")
