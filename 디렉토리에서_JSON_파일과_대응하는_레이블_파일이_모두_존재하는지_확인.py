import os  # 운영체제와 상호작용하기 위한 모듈. 디렉토리 내 파일을 처리하는 데 사용됩니다.

# 디렉토리 설정
json_dir = 'yourpath/to/json'  # JSON 파일들이 위치한 디렉토리 경로입니다.
label_dir = 'yourpath/to/labels'  # 레이블 파일들이 위치한 디렉토리 경로입니다.

# JSON 파일 목록 생성
# json_dir 디렉토리 내의 모든 .json 파일의 파일명(확장자 제외)을 집합으로 생성합니다.
# 예를 들어, 'example.json' 파일은 'example'로 변환되어 집합에 추가됩니다.
json_files = {os.path.splitext(f)[0] for f in os.listdir(json_dir) if f.endswith('.json')}

# 레이블 파일 목록 생성
# label_dir 디렉토리 내의 모든 .txt 파일의 파일명(확장자 제외)을 집합으로 생성합니다.
# 예를 들어, 'example.txt' 파일은 'example'로 변환되어 집합에 추가됩니다.
label_files = {os.path.splitext(f)[0] for f in os.listdir(label_dir) if f.endswith('.txt')}

# 누락된 레이블 파일 찾기
# json_files 집합에 포함되어 있지만 label_files 집합에는 없는 파일명을 찾습니다.
# 예를 들어, 'example'이 json_files에는 있지만 label_files에는 없는 경우를 찾습니다.
missing_labels = json_files - label_files

# 결과 출력
if missing_labels:
    # 누락된 레이블 파일이 있는 경우, 해당 파일들의 목록을 출력합니다.
    print("Missing label files for the following JSON files:")
    for missing_label in missing_labels:
        # 누락된 레이블 파일의 파일명을 출력합니다.
        print(f"{missing_label}.json")
else:
    # 모든 JSON 파일에 대응하는 레이블 파일이 있는 경우
    print("All JSON files have corresponding label files.")
