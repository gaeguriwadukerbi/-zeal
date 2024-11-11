import sqlite3  # sqlite3 모듈을 가져와서 SQLite 데이터베이스와 상호작용할 수 있도록 함

# 데이터베이스 연결 생성
# 'example.db'라는 파일을 데이터베이스로 사용하며, 파일이 없으면 새로 생성됨
conn = sqlite3.connect("example.db")

# 커서 객체 생성
# 커서는 데이터베이스와 상호작용(쿼리 실행 등)할 때 사용하는 객체임
cursor = conn.cursor()

# 테이블 생성
# 'items'라는 테이블을 생성하며, 각 컬럼의 이름과 데이터 타입을 정의함
# PRIMARY KEY 설정된 id는 각 항목에 대한 고유 식별자로 사용됨
# IF NOT EXISTS를 사용하여 이미 테이블이 존재할 경우 테이블을 다시 생성하지 않음
cursor.execute("""
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY,  # 고유 식별자 역할을 하는 정수형 id 컬럼
    name TEXT,               # 항목의 이름을 저장하는 텍스트형 name 컬럼
    price REAL,              # 항목의 가격을 저장하는 실수형 price 컬럼
    image BLOB               # 항목의 이미지 데이터를 저장하는 바이너리형 image 컬럼
)
""")

# 데이터 삽입
# 파일을 열어 이미지 데이터를 읽어오고 데이터베이스에 삽입
# "example_image.jpg" 파일을 바이너리 모드로 열어 파일 내용을 image_data 변수에 저장
with open("example_image.jpg", "rb") as file:  # 이미지 파일을 바이너리 모드로 읽음
    image_data = file.read()  # 파일 내용을 읽어서 image_data에 저장

# INSERT INTO 구문을 통해 items 테이블에 데이터를 삽입
# (name, price, image) 순서에 맞게 각각 값을 삽입
# '?'는 SQL 구문에서 자리 표시자로 사용되어 각 데이터는 튜플로 전달됨
cursor.execute("INSERT INTO items (name, price, image) VALUES (?, ?, ?)", 
               ("Laptop", 999.99, image_data))

# 데이터 조회
# SELECT 구문을 사용하여 items 테이블의 name과 price 컬럼 데이터를 조회
# 모든 행의 결과를 리스트 형식으로 반환받아 출력
cursor.execute("SELECT name, price FROM items")
print(cursor.fetchall())  # 예시 출력: [('Laptop', 999.99)]

# 변경사항 저장
# SQLite는 기본적으로 모든 변경사항을 메모리에만 유지하고 있기 때문에 commit()을 호출하여 변경사항을 파일에 저장
conn.commit()

# 데이터베이스 연결 종료
# 더 이상 데이터베이스와의 연결이 필요 없으므로 close()를 호출하여 연결을 종료
conn.close()