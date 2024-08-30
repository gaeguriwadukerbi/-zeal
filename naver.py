import os
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.by import By

def main():
    # WebDriver 옵션 설정
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # WebDriver 초기화 (Selenium Manager가 자동으로 드라이버 관리)
    driver = webdriver.Chrome(options=options)

    # 네이버 날씨 페이지로 이동
    driver.get("https://search.naver.com/search.naver?query=%EB%82%A0%EC%94%A8")
    driver.implicitly_wait(10)

    # 날씨 섹션 요소 선택 및 스크린샷 촬영
    section = driver.find_element(By.CSS_SELECTOR, "#main_pack > section.sc_new.cs_weather_new._cs_weather > div > div:nth-child(1) > div.content_wrap > div.open > div:nth-child(1)")
    section_screenshot = section.screenshot_as_png

    # 스크린샷 이미지 저장
    img = Image.open(BytesIO(section_screenshot))
    current_dir = os.path.dirname(os.path.abspath(__file__))
    img.save(os.path.join(current_dir, "Result.png"))
    print("Image has been saved as 'Result.png' in the current directory.")

    # HTML 파일 생성 및 저장
    with open(os.path.join(current_dir, "Result.html"), "w", encoding="utf-8") as file:
        file.write(f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <title>Result</title>
        <style>
        .cs_weather_new, .cs_weather_new * {{
            font-size: 0.7rem !important;
        }}
        </style>
        </head>
        <body>
        <img src="Result.png" alt="Result Section">
        </body>
        </html>
        """)
    print("HTML has been saved as 'Result.html' in the current directory.")

    # WebDriver 종료
    driver.quit()

if __name__ == "__main__":
    main()