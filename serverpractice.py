from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

class TextStoreHTTPRequestHandler(BaseHTTPRequestHandler):
    storage_file = "stored_text.txt"
    
    def do_GET(self):
        """GET 요청 처리: 저장된 텍스트 데이터를 반환합니다."""
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        
        try:
            with open(self.storage_file, 'r', encoding='utf-8') as f:
                stored_text = f.read()
            self.wfile.write(stored_text.encode('utf-8'))
        except FileNotFoundError:
            self.wfile.write(b"No text has been stored yet.")
    
    def do_POST(self):
        """POST 요청 처리: 텍스트 데이터를 받아서 파일에 저장합니다."""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        decoded_data = urllib.parse.unquote(post_data.decode('utf-8'))
        
        with open(self.storage_file, 'w', encoding='utf-8') as f:
            f.write(decoded_data)
        
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(b"Text has been stored successfully.")

def run(server_class=HTTPServer, handler_class=TextStoreHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting text store server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
