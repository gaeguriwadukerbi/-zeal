import os
import json
import datetime

import streamlit as st
import ollama

try:
    OLLAMA_MODELS = ollama.list()["models"]
except Exception as e:
    st.warning("Please make sure Ollama is installed first. See https://ollama.ai for more details.")
    st.stop()

def st_ollama(model_name, user_question, chat_history_key, params):
    if chat_history_key not in st.session_state.keys():
        st.session_state[chat_history_key] = []

    print_chat_history_timeline(chat_history_key)
        
    if user_question:
        st.session_state[chat_history_key].append({"content": f"{user_question}", "role": "user"})
        with st.chat_message("question", avatar="🧑‍🚀"):
            st.write(user_question)

        # 파라미터 출력
        with st.chat_message("parameters", avatar="🔧"):
            st.write("Ollama Parameters:")
            for key, value in params.items():
                if key != "system":  # 시스템 프롬프트는 별도로 표시
                    st.write(f"{key}: {value}")
            st.write(f"System Prompt: {params.get('system', 'None')}")

        messages = [dict(content=message["content"], role=message["role"]) for message in st.session_state[chat_history_key]]
        
        # 시스템 프롬프트가 있으면 메시지 리스트의 시작 부분에 추가
        if params.get("system"):
            messages.insert(0, {"role": "system", "content": params["system"]})

        def llm_stream(response):
            response = ollama.chat(
                model_name, 
                messages, 
                stream=True,
                options={k: v for k, v in params.items() if k != "system"}  # system 프롬프트는 options에서 제외
            )
            for chunk in response:
                yield chunk['message']['content']

        with st.chat_message("response", avatar="🤖"):
            chat_box = st.empty()
            response_message = chat_box.write_stream(llm_stream(messages))

        st.session_state[chat_history_key].append({"content": f"{response_message}", "role": "assistant"})
        
        return response_message

def print_chat_history_timeline(chat_history_key):
    for message in st.session_state[chat_history_key]:
        role = message["role"]
        if role == "user":
            with st.chat_message("user", avatar="🧑‍🚀"): 
                question = message["content"]
                st.markdown(f"{question}", unsafe_allow_html=True)
        elif role == "assistant":
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(message["content"], unsafe_allow_html=True)

def assert_models_installed():
    if len(OLLAMA_MODELS) < 1:
        st.sidebar.warning("No models found. Please install at least one model e.g. `ollama run llama2`")
        st.stop()

def select_model(key):
    model_names = ["선택안함"] + [model["name"] for model in OLLAMA_MODELS]
    default_index = model_names.index('gemma2:9b') if 'gemma2:9b' in model_names else 0
    llm_name = st.sidebar.selectbox(f"Choose Agent for {key}", model_names, index=default_index, key=f"model_select_{key}")
    if llm_name and llm_name != "선택안함":
        llm_details = [model for model in OLLAMA_MODELS if model["name"] == llm_name][0]
        if type(llm_details["size"]) != str:
            llm_details["size"] = f"{round(llm_details['size'] / 1e9, 2)} GB"
        with st.expander(f"LLM Details for {key}"):
            st.write(llm_details)
    return llm_name

def save_conversation(llm_name, conversation_key):
    OUTPUT_DIR = "llm_conversations"
    OUTPUT_DIR = os.path.join(os.getcwd(), OUTPUT_DIR)
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{OUTPUT_DIR}/{timestamp}_{llm_name.replace(':', '-')}"

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    if st.session_state[conversation_key]:
        if st.sidebar.button(f"Save conversation {conversation_key}"):
            with open(f"{filename}_{conversation_key}.json", "w") as f:
                json.dump(st.session_state[conversation_key], f, indent=4)
            st.success(f"Conversation saved to {filename}_{conversation_key}.json")

if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="Ollama Chat", page_icon="🦙")

    st.sidebar.title("Ollama Chat 🦙")
    
    assert_models_installed()

    # Model 1 선택
    llm_name_1 = select_model("Model 1")
    
    # Model 2 선택
    llm_name_2 = select_model("Model 2")

    # Model 1 Parameters
    # Model 1 Parameters
    params_1 = {}
    if llm_name_1 != "선택안함":
        st.sidebar.subheader("Model 1 Parameters")
        system_prompt_1 = st.sidebar.text_area("System Prompt for Model 1", "사용자의 문장을 완성하세요. 반드시 한 문장으로 작성하세요. 결과만 제공해주세요.", help="모델의 전반적인 행동을 지시. 구체적일수록 원하는 결과를 얻기 쉬움", height=100)
        params_1 = {
            "system": system_prompt_1,
            "num_predict": st.sidebar.number_input("Max Tokens (num_predict) 1", min_value=1, max_value=2048, value=1024, step=1, help="생성할 최대 토큰 수. 높을수록 긴 응답, 낮을수록 짧은 응답"),
            "temperature": st.sidebar.slider("Temperature 1", 0.0, 2.0, 0.0, 0.1, help="높을수록 창의성과 다양성 증가, 낮을수록 일관성과 정확성 증가"),
            "top_k": st.sidebar.slider("Top K 1", 1, 100, 40, 1, help="다음 토큰 선택 시 고려할 상위 K개의 토큰. 높을수록 다양성 증가, 낮을수록 정확성 증가"),
            "top_p": st.sidebar.slider("Top P 1", 0.0, 1.0, 0.9, 0.05, help="누적 확률 P에 해당하는 상위 토큰만 고려. 1에 가까울수록 다양성 증가, 0에 가까울수록 정확성 증가"),
            "repeat_penalty": st.sidebar.slider("Repeat Penalty 1", 0.0, 2.0, 1.1, 0.1, help="단어 반복 억제. 높을수록 반복 감소, 낮을수록 자연스러운 반복 허용"),
            "presence_penalty": st.sidebar.slider("Presence Penalty 1", 0.0, 2.0, 0.0, 0.1, help="새로운 주제 도입 장려. 높을수록 새로운 주제 도입 증가, 낮을수록 기존 주제 유지"),
            "frequency_penalty": st.sidebar.slider("Frequency Penalty 1", 0.0, 2.0, 0.0, 0.1, help="자주 사용된 단어 억제. 높을수록 다양한 어휘 사용, 낮을수록 자연스러운 단어 빈도 유지"),
            "stop": st.sidebar.text_input("Stop Sequences 1 (comma-separated)", "", help="생성 중단 시퀀스. 여러 개 입력 시 쉼표로 구분"),
            "seed": 1
        }
        params_1["stop"] = [s.strip() for s in params_1["stop"].split(',') if s.strip()]

    # Model 2 Parameters
    params_2 = {}
    if llm_name_2 != "선택안함":
        st.sidebar.subheader("Model 2 Parameters")
        system_prompt_2 = st.sidebar.text_area("System Prompt for Model 2", "사용자의 문장을 완성하세요. 반드시 한 문장으로 작성하세요. 결과만 제공해주세요.", help="모델의 전반적인 행동을 지시. 구체적일수록 원하는 결과를 얻기 쉬움", height=100)
        params_2 = {
            "system": system_prompt_2,
            "num_predict": st.sidebar.number_input("Max Tokens (num_predict) 2", min_value=1, max_value=2048, value=1024, step=1, help="생성할 최대 토큰 수. 높을수록 긴 응답, 낮을수록 짧은 응답"),
            "temperature": st.sidebar.slider("Temperature 2", 0.0, 2.0, 2.0, 0.1, help="높을수록 창의성과 다양성 증가, 낮을수록 일관성과 정확성 증가"),
            "top_k": st.sidebar.slider("Top K 2", 1, 100, 40, 1, help="다음 토큰 선택 시 고려할 상위 K개의 토큰. 높을수록 다양성 증가, 낮을수록 정확성 증가"),
            "top_p": st.sidebar.slider("Top P 2", 0.0, 1.0, 0.9, 0.05, help="누적 확률 P에 해당하는 상위 토큰만 고려. 1에 가까울수록 다양성 증가, 0에 가까울수록 정확성 증가"),
            "repeat_penalty": st.sidebar.slider("Repeat Penalty 2", 0.0, 2.0, 1.1, 0.1, help="단어 반복 억제. 높을수록 반복 감소, 낮을수록 자연스러운 반복 허용"),
            "presence_penalty": st.sidebar.slider("Presence Penalty 2", 0.0, 2.0, 0.0, 0.1, help="새로운 주제 도입 장려. 높을수록 새로운 주제 도입 증가, 낮을수록 기존 주제 유지"),
            "frequency_penalty": st.sidebar.slider("Frequency Penalty 2", 0.0, 2.0, 0.0, 0.1, help="자주 사용된 단어 억제. 높을수록 다양한 어휘 사용, 낮을수록 자연스러운 단어 빈도 유지"),
            "stop": st.sidebar.text_input("Stop Sequences 2 (comma-separated)", "", help="생성 중단 시퀀스. 여러 개 입력 시 쉼표로 구분"),
            "seed": 41
        }
        params_2["stop"] = [s.strip() for s in params_2["stop"].split(',') if s.strip()]

    prompt = st.chat_input("Ask a question ...")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Model 1 Output")
        if llm_name_1 != "선택안함":
            conversation_key_1 = f"model_{llm_name_1}_1"
            st_ollama(llm_name_1, prompt, conversation_key_1, params_1)
            
            # Clear and Save buttons for Model 1
            if st.session_state.get(conversation_key_1):
                clear_conversation_1 = st.sidebar.button("Clear chat 1")
                if clear_conversation_1:
                    st.session_state[conversation_key_1] = []
                    st.rerun()
            save_conversation(llm_name_1, conversation_key_1)
        else:
            st.write("모델이 선택되지 않았습니다.")

    with col2:
        st.subheader("Model 2 Output")
        if llm_name_2 != "선택안함":
            conversation_key_2 = f"model_{llm_name_2}_2"
            st_ollama(llm_name_2, prompt, conversation_key_2, params_2)
            
            # Clear and Save buttons for Model 2
            if st.session_state.get(conversation_key_2):
                clear_conversation_2 = st.sidebar.button("Clear chat 2")
                if clear_conversation_2:
                    st.session_state[conversation_key_2] = []
                    st.rerun()
            save_conversation(llm_name_2, conversation_key_2)
        else:
            st.write("모델이 선택되지 않았습니다.")