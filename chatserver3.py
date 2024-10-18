from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests

# Ollama 모델에 질문하기
def query_to_gemma(input_text):
    url = "http://localhost:11434/api/generate"
    about_model = {
        "model": "gemma2:9b",
        "prompt": input_text,
        "stream": False
    }
    headers = {"content-type": "application/json"}
    response = requests.post(url, json=about_model, headers=headers)
    if response.status_code == 200:
        return response.json()["response"]
    else:
        return f"오류 발생: {response.status_code}"

# HTTP 서버 구현
class Post_office(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')

        # Ollama 모델에 질문하고 응답 생성
        model_response = query_to_gemma(post_data)

        self.send_response(200)
        self.send_header('Content-type', 'application/json;charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps({"Yes_Man": model_response}, ensure_ascii=False).encode('utf-8'))

# 서버 실행
def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, Post_office)
    print('서버 실행 중...')
    httpd.serve_forever()

run_server()
