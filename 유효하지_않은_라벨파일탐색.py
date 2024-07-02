import os  # 운영체제와 상호작용하기 위한 모듈. 디렉토리 내 파일을 처리하는 데 사용됩니다.

# 레이블 파일들이 위치한 디렉토리 경로 설정
label_dir = 'yourpath/to/labels'  # 레이블 파일들이 위치한 디렉토리 경로입니다.

# 유효하지 않은 레이블 파일 경로를 저장할 리스트 초기화
invalid_labels = []  # 유효하지 않은 레이블 파일 경로를 저장할 리스트를 초기화합니다.

# 레이블 파일 검사
# 지정된 디렉토리 내의 모든 파일을 목록으로 가져옵니다.
for label_file in os.listdir(label_dir):
    # 파일이 .txt로 끝나는지 확인하여 레이블 파일인지 확인합니다.
    if label_file.endswith('.txt'):
        # 레이블 파일의 전체 경로를 생성합니다.
        label_path = os.path.join(label_dir, label_file)
        # 레이블 파일을 읽기 모드로 엽니다.
        with open(label_path, 'r') as file:
            lines = file.readlines()  # 파일의 모든 줄을 읽어들입니다.
            # 각 줄에서 클래스 ID를 추출하여 유효성 검사를 합니다.
            for line in lines:
                try:
                    # 클래스 ID를 추출합니다. 예를 들어, "0 0.5 0.5 1 1"에서 첫 번째 값인 0을 추출합니다.
                    class_id = int(float(line.split()[0]))
                    if class_id >= 2:  # 클래스 ID가 2 이상인 경우
                        invalid_labels.append(label_path)  # 유효하지 않은 레이블 파일 목록에 추가합니다.
                        break  # 더 이상 검사하지 않고 다음 파일로 넘어갑니다.
                except ValueError as e:  # 클래스 ID 추출 중 오류가 발생한 경우
                    # 오류 메시지를 출력하고 해당 파일을 유효하지 않은 레이블 파일 목록에 추가합니다.
                    print(f"Error processing {label_path}: {e}")
                    invalid_labels.append(label_path)  # 유효하지 않은 레이블 파일 목록에 추가합니다.
                    break  # 더 이상 검사하지 않고 다음 파일로 넘어갑니다.

# 유효하지 않은 레이블 파일이 있는 경우, 해당 파일들의 경로를 출력합니다.
if invalid_labels:
    print("Invalid label files found:")
    for label_path in invalid_labels:
        print(label_path)
else:
    print("All labels are valid.")  # 유효하지 않은 레이블 파일이 없는 경우
