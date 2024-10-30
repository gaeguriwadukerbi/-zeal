import requests

def call_Yes_Man():
    print("Yes_Man이 호출되었습니다. 'good bye'를 입력하면 종료됩니다.")
    conversation_history = ""  # 이전 대화 내용을 저장할 변수
    
    while True:
        user_input = input("Courier: ")
        
        if user_input.lower() == 'good bye':
            print("대화를 종료합니다.")
            break
        
        # 대화 내용에 추가 (Yes Man의 이전 응답은 그대로 유지)
        conversation_history += f"Courier: {user_input}\n"
        
        # 서버로 POST 요청 보내기
        response = requests.post("http://localhost:7777", data=conversation_history)
        
        if response.status_code == 200:
            response_text = response.json()["Yes_Man"]
            print("Yes_Man:", response_text)
            # 응답을 대화 로그에 추가
            conversation_history += f"Yes Man: {response_text}\n"
        else:
            print("오류 발생:", response.status_code)

# 채팅 함수 실행
call_Yes_Man()
