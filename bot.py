from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests

def query_to_gemma(input_text):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "gemma2:9b",
        "prompt": input_text
    }
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        
        # Ollama API returns a stream of JSON objects, we need to parse them line by line
        response_text = ""
        for line in response.iter_lines():
            if line:
                json_response = json.loads(line)
                if 'response' in json_response:
                    response_text += json_response['response']
        
        return response_text
    except requests.RequestException as e:
        print(f"Error querying Gemma: {e}")
        return '오류 발생, 재시도 바람'
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return '오류 발생, JSON 디코딩 실패'

text_data = ""

class PostOffice(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        response = {"user_input": text_data, "model_response": query_to_gemma(text_data)}
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))

    def do_POST(self):
        global text_data
        content_length = int(self.headers['Content-Length'])
        text_data = self.rfile.read(content_length).decode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write('요청 받음'.encode('utf-8'))

def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, PostOffice)
    print('서버 실행 중')
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()