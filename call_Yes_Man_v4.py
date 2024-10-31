import requests
import streamlit as st

def call_Yes_Man():
    st.title("Yes_Man이 호출되었습니다. 'good bye'를 입력하면 종료됩니다.")
    
    # 기존 코드의 conversation_history 변수를 session_state로 변환
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = ""
    
    # 기존의 input() 함수를 streamlit의 text_input으로 변환
    user_input = st.text_input("Courier:", key="user_input")
    
    if user_input:
        if user_input.lower() == 'good bye':
            st.write("대화를 종료합니다.")
            st.session_state.conversation_history = ""  # 대화 기록 초기화
            st.experimental_rerun()
            return
        
        # 기존 코드와 동일한 방식으로 대화 기록 관리
        st.session_state.conversation_history += f"Courier: {user_input}\n"
        
        # 기존 코드와 동일한 서버 통신
        response = requests.post("http://localhost:7777", 
            data=st.session_state.conversation_history)
        
        if response.status_code == 200:
            response_text = response.json()["Yes_Man"]
            st.session_state.conversation_history += f"Yes Man: {response_text}\n"
            
            # 대화 기록 표시
            for line in st.session_state.conversation_history.split('\n'):
                if line:  # 빈 줄 제외
                    st.write(line)
            
            # 입력 필드 초기화
            st.text_input("Courier:", value="", key="user_input_clear")
            st.experimental_rerun()
        else:
            st.error(f"오류 발생: {response.status_code}")

# 기존 코드의 실행 부분을 유지
call_Yes_Man()