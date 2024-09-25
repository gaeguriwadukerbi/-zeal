from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def main():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")  # GPU 가속 비활성화
    options.add_argument("--no-sandbox")  # 샌드박스 모드 비활성화
    options.add_argument("--disable-dev-shm-usage")  # /dev/shm 파티션 사용 비활성화

    options.headless = True  # 브라우저를 헤드리스 모드로 실행
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # 네이버 날씨 검색 결과 페이지에 접속
    driver.get("https://search.naver.com/search.naver?query=날씨")
    driver.implicitly_wait(10)  # 페이지 로드를 기다림

    # 원하는 요소의 HTML 추출
    element = driver.find_element(By.CSS_SELECTOR, "section.sc_new.cs_weather_new._cs_weather")
    extracted_html = element.get_attribute('outerHTML')

    # HTML 파일에 추출된 내용을 포함하여 저장
    with open("extracted_weather.html", "w", encoding="utf-8") as file:
        file.write(f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Extracted Weather Section</title>
    <link rel="stylesheet" type="text/css" href="https://ssl.pstatic.net/sstatic/keypage/outside/scui/weather_new_new/css/cs_weahter_new_231129.css">
    <style>
        /* 모든 요소의 폰트 크기를 감소시키는 CSS */
        .cs_weather_new, .cs_weather_new * {{
            font-size: 0.8rem !important;
        }}
    </style>
</head>
<body>
    {extracted_html}
</body>
</html>
""")
        print("HTML has been saved as 'extracted_weather.html'")

    driver.quit()

if __name__ == "__main__":
    main()
