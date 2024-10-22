import requests

def call_Yes_Man():
    print("Yes_Man과 대화를 시작합니다. 'good bye'를 입력하면 종료됩니다.")
    while True:
        # 사용자로부터 입력 받기
        user_input = input("You: ")
        
        # 종료 조건
        if user_input.lower() == 'good bye':
            print("대화를 종료합니다.")
            break
        
        # 서버로 POST 요청 보내기
        response = requests.post("http://localhost:8000", data=user_input)
        
        # 서버로부터 받은 응답 출력
        if response.status_code == 200:
            print("Yes_Man:", response.json()["Yes_Man"])
        else:
            print("오류 발생:", response.status_code)

# 채팅 함수 실행
call_Yes_Man()
