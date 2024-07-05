from flask import Flask, request, jsonify

app = Flask(__name__)

# 데이터를 저장할 리스트
saved_texts = []

@app.route('/save_text', methods=['POST'])
def save_text():
    # JSON 형식의 요청에서 'text' 값을 추출
    text = request.json.get('text')
    if text:
        saved_texts.append(text)
        return jsonify({"message": "Text saved successfully!"}), 200
    else:
        return jsonify({"message": "No text provided!"}), 400

@app.route('/get_texts', methods=['GET'])
def get_texts():
    return jsonify({"saved_texts": saved_texts}), 200

if __name__ == '__main__':
    app.run(debug=True)
