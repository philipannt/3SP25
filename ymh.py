import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

url = "https://yamaha-motor.com.vn/xe/?filter=eyJjYXRlIjpbInhlLXRheS1nYSIsInhlLXNvIl0sInByaWNlIjoiNTs2MDAifQ=="
driver.get(url)

wait = WebDriverWait(driver, 15)

bike_elements = driver.find_elements(By.CLASS_NAME, "js-filter-result")

data = []

for bike in bike_elements:
    try:
        brand = "Yamaha"
        name = bike.find_element(By.CLASS_NAME, "c-prodbox__ttl").text.strip()
        price_element = driver.find_element(By.CSS_SELECTOR, ".c-prodbox__price strong")
        price = re.sub(r"[^\d]", "", price_element)
        url = bike.find_element(By.TAG_NAME, "a").get_attribute("href")

        data.append([brand, name, price, url])

    except Exception as e:
        print(f"Lỗi khi lấy dữ liệu: {e}")

driver.quit()

df = pd.DataFrame(data, columns=["Thương hiệu", " Model", " Giá", " Link"])
df.to_csv("yamaha.csv", index=False, encoding="utf-8-sig")

print("Done")