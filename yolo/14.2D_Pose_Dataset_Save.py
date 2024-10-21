import pandas as pd
import os

# 저장 경로 설정
save_dir = './pose_img/person/'
keypoint_path = f'{save_dir}keypoints.csv'  # 확장자 수정
dataset_dir = f'{save_dir}/'

# 폴더 이름 설정
str_sitting = 'sitting_pose'
str_standing = 'standing_pose'

# CSV 파일 로드
df = pd.read_csv(keypoint_path)

# 앉아있는 이미지와 서있는 이미지 경로 설정
sitting_path = os.path.join(dataset_dir, str_sitting)
standing_path = os.path.join(dataset_dir, str_standing)

# 이미지 이름에 따라 레이블을 지정하는 함수 정의
def get_label(image_name, sitting_path, standing_path):
    if image_name in os.listdir(sitting_path):
        return 'sitting'
    elif image_name in os.listdir(standing_path):
        return 'standing'
    else:
        return None  # 폴더에 이미지가 없는 경우 None 반환

# CSV 파일에 'label' 열 추가
df['label'] = df['image_name'].apply(lambda x: get_label(x, sitting_path, standing_path))

# 레이블이 없는 데이터 필터링 (None 제거)
df = df.dropna(subset=['label'])

# 새로운 CSV 파일로 저장
df.to_csv(f'{dataset_dir}dataset.csv', index=False)
