from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def main():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get("https://search.naver.com/search.naver?query=날씨")
    driver.implicitly_wait(10)  # 페이지 로드를 기다림

    # 전체 섹션 요소를 가져옵니다.
    section = driver.find_element(By.CSS_SELECTOR, "section.sc_new.cs_weather_new._cs_weather")

    # 제외할 선택자 목록
    exclude_selectors = [
        "div > div:nth-child(1) > div.top_wrap > div.title_area._area_panel > h2.blind",
        "div > div:nth-child(1) > div.content_wrap > div.open > div:nth-child(2) > div > div > div.sub_tab > div > ul > li:nth-child(1) > a > span",
        "div > div:nth-child(1) > div.content_wrap > div.open > div:nth-child(2) > div > div > div.sub_tab > div > ul > li:nth-child(2) > a > span",
        "div > div:nth-child(1) > div.content_wrap > div.open > div:nth-child(2) > div > div > div.sub_tab > div > ul > li:nth-child(3) > a > span",
        "div > div:nth-child(1) > div.content_wrap > div.open > div:nth-child(2) > div > div > div.sub_tab > div > ul > li:nth-child(4) > a > span",
        "div > div:nth-child(2) > div.content_wrap > div > div.inner > div > h3",
        "div > div:nth-child(2) > div.content_wrap > div > div.inner > div > div.weather_refer > a > i > span",
        "div > div:nth-child(2) > div.content_wrap > div > div.inner > div > a > span",
        "div > div:nth-child(2) > div.content_wrap > div > div.inner > div > div.notice_info > p",
        "div > div:nth-child(1) > div.top_wrap > div.sub_tab_area > div > div > ul",
        "div > div:nth-child(1) > div.content_wrap > div.open > div:nth-child(1) > div > div.multi_cp_area.__web-inspector-hide-shortcut__"
    ]

    # 제외할 요소를 찾아 HTML에서 제거
    for sel in exclude_selectors:
        elements_to_exclude = section.find_elements(By.CSS_SELECTOR, sel)
        for element in elements_to_exclude:
            driver.execute_script("var element = arguments[0]; element.parentNode.removeChild(element);", element)

    # 수정된 section의 HTML 추출
    modified_html = section.get_attribute('outerHTML')

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
    {modified_html}
</body>
</html>
""")
        print("HTML has been saved as 'extracted_weather.html'")

    driver.quit()

if __name__ == "__main__":
    main()
