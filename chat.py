import streamlit as st
import json
import requests
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableMap

# API 호출 함수
def get_air_quality_data(sido, service_key, num_of_rows=100, page_no=1, version='1.0', return_type='json'):
    url = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty'
    params = {
        'serviceKey': service_key,
        'returnType': return_type,
        'numOfRows': str(num_of_rows),
        'pageNo': str(page_no),
        'sidoName': sido,
        'ver': version
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        try:
            data = json.loads(content)
            return data
        except json.JSONDecodeError:
            st.error("데이터를 처리하는 데 실패했습니다.")
            return None
    else:
        st.error(f"API 호출 실패: {response.status_code}")
        return None

# 대기질 정보를 대화 형식으로 가공
def process_air_quality_data(data):
    if data and data['response']['body']['totalCount'] > 0:
        items = data['response']['body']['items']
        conversation_data = []
        for item in items:
            station_name = item['stationName']
            pm10 = item['pm10Value']
            pm25 = item['pm25Value']
            o3 = item['o3Value']
            khai = item['khaiValue']
            conversation_data.append(
                f"측정소: {station_name}, PM10: {pm10}, PM2.5: {pm25}, 오존: {o3}, 종합대기질: {khai}"
            )
        return conversation_data
    else:
        return ["해당 시/도에 대한 데이터를 찾을 수 없습니다."]

# Streamlit UI 구성 및 챗봇 응답 처리
def main():
    st.title("대기질 정보 제공 챗봇")
    
    # 사용자가 시/도 이름 입력
    sido = st.text_input("시/도 이름을 입력하세요:", value="서울")
    
    # 사용자가 데이터를 요청하면 API 호출
    if st.button("대기질 정보 조회"):
        service_key = 'fLoVrDwSn9qBTNUOApqBrjY+d99UJWe32K8T77qE77kvTXEXoHsx8KUde+p4vO+loILHU5VuVz4aXXUTuNT4Ig=='  # API 키
        data = get_air_quality_data(sido, service_key)
        
        if data:
            # LangChain을 사용해 대화 처리
            conversation_data = process_air_quality_data(data)
            
            if conversation_data:
                st.subheader(f"{sido}의 대기질 정보")
                for info in conversation_data:
                    st.write(info)

# Streamlit 앱 실행
if __name__ == "__main__":
    main()
