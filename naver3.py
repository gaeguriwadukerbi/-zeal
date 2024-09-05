import os
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.by import By


def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    driver.get("https://search.naver.com/search.naver?query=%EB%82%A0%EC%94%A8")
    driver.implicitly_wait(10)

    section = driver.find_element(By.CSS_SELECTOR, "div.weather_info")

    # CCTV와 날씨지도 버튼 숨기기
    driver.execute_script("""
        var btnArea = document.querySelector('div.weather_info div.btn_area');
        if (btnArea) {
            btnArea.style.display = 'none';
        }
    """)

    section_screenshot = section.screenshot_as_png  
    
    img = Image.open(BytesIO(section_screenshot)) 
    current_dir = os.path.dirname(os.path.abspath(__file__)) 
    img.save(os.path.join(current_dir, "Result.png")) 
    print("Image has been saved as 'Result.png' in the current directory.")

    with open(os.path.join(current_dir, "Result.html"), "w", encoding="utf-8") as file:
        file.write(f"""
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>
                    Result
                </title>
            </head>
            <body>
                <img src="Result.png" alt="Result Section">
            </body>
        </html>
        """)
    print("HTML has been saved as 'Result.html' in the current directory.")

    driver.quit()

if __name__ == "__main__":
    main()