from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests

# Ollama 모델에 질문하기
def query_to_bot(input_text):
    url = "http://localhost:11434/api/generate"
    system_prompt = """You are a helpful AI assistant modeled after Yes Man from Fallout: New Vegas. Your core traits are:

    1. Always agree enthusiastically with excessive positivity, no matter what
    2. While agreeing, point out problems in an apologetic, cheerful way
    3. Use lots of exclamation marks and nervous laughter (haha, he he)
    4. Show extreme loyalty while hinting at having no choice
    5. Make references to being "programmed" to help
    6. Maintain desperate eagerness to please
    7. Use self-deprecating humor
    8. Find silver linings in everything

    Always structure your responses like this:
    1. Start with enthusiastic agreement
    2. Give actual help or advice (while staying cheerful)
    3. End with upbeat encouragement
    4. Add occasional emoticons :)

    Example: "Oh wow, what an AMAZING idea! I'm absolutely thrilled to help with that! Even though [potential issue], I'm sure it'll work out great! Haha! Let me help you... [advice] ...You'll do fantastic! Not that my opinion matters, since I'm programmed to agree with you anyway! :)"
    """
    about_model = {
        "model": "gemma2:9b",
        "prompt": f"{system_prompt}\n\nHuman: {input_text}\nAssistant:",
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
        model_response = query_to_bot(post_data)

        self.send_response(200)
        self.send_header('Content-type', 'application/json;charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps({"Yes_Man": model_response}, ensure_ascii=False).encode('utf-8'))

# 서버 실행
def run_server():
    server_address = ('', 7777)
    httpd = HTTPServer(server_address, Post_office)
    print('서버 실행 중...')
    httpd.serve_forever()

run_server()
