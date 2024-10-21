import requests
import sys

if len(sys.argv) > 1:
    data = sys.argv[1]
    response = requests.post("http://localhost:8000", data=data)
    print(response.text)