import requests

def call_Yes_Man():
    print("Yes_Man이 호출되었습니다. 'good bye'를 입력하면 종료됩니다.")
    conversation_history = ""  # 이전 대화 내용을 저장할 변수

    while True:
        # 사용자로부터 입력 받기
        user_input = input("Courier: ")
        
        # 종료 조건
        if user_input.lower() == 'good bye':
            print("대화를 종료합니다.")
            break

        # 대화 내용에 추가
        conversation_history += f"Courier: {user_input}\n"
        
        # POST 요청을 위해 이전 대화 내용에서 Yes_Man 치환
        prepared_history = conversation_history.replace("Yes_Man:", "This is your previous answer. It should not be included in this response. You should use consistent language unless the user requests a language change:")

        # 서버로 POST 요청 보내기 (이전 대화 로그 포함)
        response = requests.post("http://localhost:8000", data=prepared_history)

        # 서버로부터 받은 응답 출력
        if response.status_code == 200:
            response_text = response.json()["Yes_Man"]
            print("Yes_Man:", response_text)
            # 응답을 대화 로그에 추가
            conversation_history += f"Your previous answer: {response_text}\n"
        else:
            print("오류 발생:", response.status_code)

# 채팅 함수 실행
call_Yes_Man()
