'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
try:
    driver.get("https://www.naver.com")
    search_box = driver.find_element(By.ID, 'query')
    search_box.send_keys("날씨", Keys.ENTER)
    driver.implicitly_wait(10)
    try:
        weather_summary = driver.find_element(By.CLASS_NAME, 'temperature_info')
        print(weather_summary.text)
    except NoSuchElementException:
        print("Weather summary not found.")
    try:
        additional_info = driver.find_elements(By.CLASS_NAME, 'report_card_wrap')
        for info in additional_info:
            print(info.text) 
    except NoSuchElementException:
        print("Additional weather information not found.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()
'''
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
try:
    driver.get("https://www.naver.com")
    search_box = driver.find_element(By.ID, 'query')
    search_box.send_keys("날씨", Keys.ENTER)
    driver.implicitly_wait(10)
    try:
        weather_summary = driver.find_element(By.CLASS_NAME, 'temperature_info')
        print(weather_summary.text)
    except NoSuchElementException:
        print("Weather summary not found.")
    try:
        additional_info = driver.find_elements(By.CLASS_NAME, 'report_card_wrap')
        for info in additional_info:
            print(info.text)
    except NoSuchElementException:
        print("Additional weather information not found.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()
'''
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.common.exceptions import NoSuchElementException, WebDriverException

def create_driver():
    try:
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=chrome_service, options=chrome_options)
    except WebDriverException as e:
        print(f"Chrome not found, switching to Edge: {e}")
        edge_options = EdgeOptions()
        edge_options.add_argument("--headless")
        edge_service = EdgeService(EdgeChromiumDriverManager().install())
        return webdriver.Edge(service=edge_service, options=edge_options)
driver = create_driver()
try:
    driver.get("https://www.naver.com")
    search_box = driver.find_element(By.ID, 'query')
    search_box.send_keys("날씨", Keys.ENTER)
    driver.implicitly_wait(10)
    try:
        weather_summary = driver.find_element(By.CLASS_NAME, 'temperature_info')
        print(weather_summary.text)
    except NoSuchElementException:
        print("Weather summary not found.")
    try:
        additional_info = driver.find_elements(By.CLASS_NAME, 'report_card_wrap')
        for info in additional_info:
            print(info.text)
    except NoSuchElementException:
        print("Additional weather information not found.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()
'''
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions
import os

def create_driver():
    chrome_service = ChromeService(ChromeDriverManager().install())
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return driver

def fetch_weather(driver):
    driver.get("https://www.naver.com")
    search_box = driver.find_element(By.ID, 'query')
    search_box.send_keys("날씨", Keys.ENTER)
    driver.implicitly_wait(10)
    
    weather_data = {}
    try:
        weather_summary = driver.find_element(By.CLASS_NAME, 'temperature_info')
        weather_data['summary'] = weather_summary.text
    except NoSuchElementException:
        weather_data['summary'] = "Weather summary not found."
    
    try:
        additional_info = driver.find_elements(By.CLASS_NAME, 'report_card_wrap')
        weather_data['details'] = "\n".join([info.text for info in additional_info])
    except NoSuchElementException:
        weather_data['details'] = "Additional weather information not found."

    return weather_data

def save_html(data):
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
        <div class="weather-details">{data['details'].replace('\n', '<br>')}</div>
    </body>
    </html>
    """
    with open("weather_report.html", "w", encoding='utf-8') as file:
        file.write(html_content)

def main():
    driver = create_driver()
    try:
        weather_data = fetch_weather(driver)
        save_html(weather_data)
        print("HTML report has been saved.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
'''
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, WebDriverException
def set_working_directory():
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    print("Current working directory:", os.getcwd())
def create_driver():
    chrome_service = ChromeService(ChromeDriverManager().install())
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return driver
def fetch_weather(driver):
    driver.get("https://www.naver.com")
    search_box = driver.find_element(By.ID, 'query')
    search_box.send_keys("날씨", Keys.ENTER)
    driver.implicitly_wait(10)
    weather_data = {}
    try:
        weather_summary = driver.find_element(By.CLASS_NAME, 'temperature_info')
        weather_data['summary'] = weather_summary.text.replace('\n', '<br>')
    except NoSuchElementException:
        weather_data['summary'] = "Weather summary not found."
    try:
        additional_info = driver.find_elements(By.CLASS_NAME, 'report_card_wrap')
        weather_data['details'] = "<br>".join([info.text.replace('\n', '<br>') for info in additional_info])
    except NoSuchElementException:
        weather_data['details'] = "Additional weather information not found."
    return weather_data
def save_html(data):
    file_name = 'weather_report.html'
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
        <h1>top area</h1>
        <div class="weather-summary">{data['summary']}</div>
        <h2>bot area</h2>
        <div class="weather-details">{data['details']}</div>
    </body>
    </html>
    """
    with open(file_name, "w", encoding='utf-8') as file:
        file.write(html_content)
    print(f"HTML report has been saved as {file_name}")
def main():
    set_working_directory()
    driver = create_driver()
    try:
        weather_data = fetch_weather(driver)
        save_html(weather_data)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
if __name__ == "__main__":
    main()
