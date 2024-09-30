from http.server import BaseHTTPRequestHandler, HTTPServer 
import json 
import requests 

def query_to_gemma(input_text): 
    url = "http://localhost:11434/api/generate" 
    about_model = { 
        "model" : "gemma2:9b", 
        "prompt" : input_text,
        "stream" : False
    } 
    header = { 
        "content-type" : "application/json" 
    } 
    response = requests.post(url,json=about_model, headers=header) 
    if response.status_code ==200: #200 OK는 HTTP 요청이 성공 
        return response.json()["response"] 
    else: return '오류발생' 

text_data = "" 

class post_office(BaseHTTPRequestHandler): 

    def do_GET(self): 
        self.send_response(200) 
        self.send_header('Content-type', 'application/json;charset=utf-8') 
        self.end_headers() 
        response = {"user_input" : text_data,"model_response" : query_to_gemma(text_data)} 
        self.wfile.write(json.dumps(response).encode('utf-8')) 

    def do_POST(self): 
        global text_data 
        content_length = int(self.headers['Content-Length']) 
        receive_data = self.rfile.read(content_length).decode('utf-8') 
        text_data = receive_data 
        self.send_response(200) 
        self.send_header('content-type', 'text/plain; charset=utf-8') 
        self.end_headers() 
        self.wfile.write('메세지 수신'.encode('utf-8')) 

def server(): 
    server_address = ('', 8000) 
    httpd = HTTPServer(server_address, post_office) 
    print('서버 실행 중') 
    httpd.serve_forever() 

server()