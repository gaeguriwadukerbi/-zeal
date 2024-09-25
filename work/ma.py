from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def main():
    options = Options()
    options.headless = True
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # 네이버 날씨 검색 결과 페이지에 접속
    driver.get("https://search.naver.com/search.naver?query=날씨")
    driver.implicitly_wait(10)

    # 전체 섹션 요소를 가져옵니다.
    section = driver.find_element(By.CSS_SELECTOR, "#main_pack > section.sc_new.cs_weather_new._cs_weather")

    # 제외할 선택자 목록
    exclude_selectors = [
        "> div > div:nth-child(1) > div.top_wrap > div.title_area._area_panel > h2.blind",
        "> div > div:nth-child(1) > div.content_wrap > div.open > div:nth-child(2) > div > div > div.sub_tab > div > ul > li:nth-child(1) > a > span",
        # 나머지 선택자들도 이 리스트에 추가...
        "> div > div:nth-child(2) > div.content_wrap > div > div.inner > div > div.notice_info > p"
    ]

    # 전체 섹션에서 모든 자식 요소를 가져옵니다.
    all_elements = section.find_elements(By.CSS_SELECTOR, "*")

    # 제외할 요소들을 필터링합니다.
    filtered_elements = [el for el in all_elements if not any(driver.execute_script("return arguments[0].matches(arguments[1])", el, section.get_attribute("css selector") + selector) for selector in exclude_selectors)]

    # 필터링된 요소들의 HTML 출력
    for element in filtered_elements:
        print(element.get_attribute('outerHTML'))

    driver.quit()

if __name__ == "__main__":
    main()
