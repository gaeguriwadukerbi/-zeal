# os 모듈을 임포트합니다. 파일 경로를 다루거나, 파일과 디렉토리 작업을 수행하는데 사용됩니다.
import os

# selenium 패키지에서 필요한 클래스와 모듈을 임포트합니다.
# webdriver를 임포트하여 웹 브라우저를 자동으로 제어할 수 있습니다.
from selenium import webdriver

# By 모듈을 사용하여 HTML 요소를 다양한 방식으로 찾을 수 있습니다. (예: ID, CLASS_NAME 등)
from selenium.webdriver.common.by import By

# Keys 모듈을 사용하여 키보드 입력을 시뮬레이션합니다. 예를 들어, 엔터 키를 누르는 등의 동작이 가능합니다.
from selenium.webdriver.common.keys import Keys

# ChromeService 클래스를 사용하여 크롬 드라이버의 인스턴스를 관리할 서비스를 생성합니다.
from selenium.webdriver.chrome.service import Service as ChromeService

# ChromeOptions 클래스를 사용하여 크롬 브라우저의 다양한 옵션을 설정할 수 있습니다. (예: headless 모드)
from selenium.webdriver.chrome.options import Options as ChromeOptions

# webdriver_manager를 통해 자동으로 크롬 드라이버를 다운로드하고 관리할 수 있는 ChromeDriverManager를 임포트합니다.
from webdriver_manager.chrome import ChromeDriverManager

# NoSuchElementException 예외는 요소를 찾을 수 없을 때 발생합니다. 이를 통해 존재하지 않는 요소에 대한 예외 처리를 할 수 있습니다.
# WebDriverException은 드라이버 관련 일반적인 예외를 처리할 때 사용됩니다.
from selenium.common.exceptions import NoSuchElementException, WebDriverException
# 작업 디렉토리를 스크립트 파일 위치로 설정하는 함수입니다.
def set_working_directory():
    # 스크립트 파일의 절대 경로를 얻습니다.
    abspath = os.path.abspath(__file__)
    # 절대 경로에서 디렉토리 경로만 추출합니다.
    dname = os.path.dirname(abspath)
    # 작업 디렉토리를 스크립트 파일의 디렉토리로 변경합니다.
    os.chdir(dname)
    # 현재 작업 디렉토리를 출력합니다.
    print("Current working directory:", os.getcwd())

# 웹 드라이버를 생성하고 설정하는 함수입니다.
def create_driver():
    # ChromeDriver를 자동으로 설치하고 관리할 ChromeService 객체를 생성합니다.
    chrome_service = ChromeService(ChromeDriverManager().install())
    # 크롬 옵션을 설정합니다. 여기서는 브라우저가 실제로 눈에 보이지 않게 headless 모드를 활성화합니다.
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")  # GPU 가속을 비활성화합니다.
    # 설정된 옵션과 서비스를 사용하여 크롬 드라이버를 초기화하고 반환합니다.
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return driver

# 네이버에서 '날씨'를 검색하고 결과를 수집하는 함수입니다.
def fetch_weather(driver):
    # 네이버의 메인 페이지로 이동합니다.
    driver.get("https://www.naver.com")
    # 검색창을 찾고 '날씨'라고 타이핑한 뒤 엔터를 쳐 검색을 수행합니다.
    search_box = driver.find_element(By.ID, 'query')
    search_box.send_keys("날씨", Keys.ENTER)
    # 페이지 로드를 위해 최대 10초 동안 대기합니다.
    driver.implicitly_wait(10)
    
    # 수집할 데이터를 저장할 딕셔너리를 초기화합니다.
    weather_data = {}
    try:
        # 날씨 정보가 요약된 부분을 찾습니다.
        weather_summary = driver.find_element(By.CLASS_NAME, 'temperature_info')
        # 찾은 요약 정보의 텍스트를 가져와 줄바꿈을 HTML 줄바꿈 태그로 변경합니다.
        weather_data['summary'] = weather_summary.text.replace('\n', '<br>')
    except NoSuchElementException:
        # 요약 정보를 찾을 수 없는 경우 예외 처리합니다.
        weather_data['summary'] = "Weather summary not found."
    
    try:
        # 추가적인 날씨 정보를 찾습니다.
        additional_info = driver.find_elements(By.CLASS_NAME, 'report_card_wrap')
        # 찾은 정보를 텍스트로 추출하고 각 정보 사이에 HTML 줄바꿈 태그를 넣어줍니다.
        weather_data['details'] = "<br>".join([info.text.replace('\n', '<br>') for info in additional_info])
    except NoSuchElementException:
        # 추가 정보를 찾을 수 없는 경우 예외 처리합니다.
        weather_data['details'] = "Additional weather information not found."

    # 수집된 날씨 데이터를 반환합니다.
    return weather_data

# 수집된 데이터를 HTML 파일로 저장하는 함수입니다.
def save_html(data):
    # 저장할 파일의 이름을 정합니다.
    file_name = 'weather_report.html'
    # HTML 내용을 작성합니다.
    html_content = f"""
    <html>
    <head>
        <title>Weather Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            .weather-summary, .weather-details {{ margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <h1>Weather Summary</h1>
        <div class="weather-summary">{data['summary']}</div>
        <h2>Additional Information</h2>
        <div class="weather-details">{data['details']}</div>
    </body>
    </html>
    """
    # 파일을 현재 디렉토리에 UTF-8 인코딩으로 저장합니다.
    with open(file_name, "w", encoding='utf-8') as file:
        file.write(html_content)
    # 저장된 파일의 위치를 출력합니다.
    print(f"HTML report has been saved as {file_name}")

# 메인 실행 함수입니다.
def main():
    set_working_directory()  # 작업 디렉토리를 설정합니다.
    driver = create_driver()  # 웹 드라이버를 생성합니다.
    try:
        weather_data = fetch_weather(driver)  # 날씨 데이터를 수집합니다.
        save_html(weather_data)  # 데이터를 HTML로 저장합니다.
    except Exception as e:
        # 오류가 발생하면 오류 메시지를 출력합니다.
        print(f"An error occurred: {e}")
    finally:
        # 모든 작업이 끝나면 웹 드라이버를 종료합니다.
        driver.quit()

# 이 스크립트가 직접 실행될 때만 main 함수를 호출합니다.
if __name__ == "__main__":
    main()
