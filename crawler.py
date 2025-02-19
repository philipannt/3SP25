import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

url = "https://www.honda.com.vn/xe-may/san-pham"
driver.get(url)

wait = WebDriverWait(driver, 15)

wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "category-item")))

bike_elements = driver.find_elements(By.CLASS_NAME, "category-item")

data = []

for bike in bike_elements:
    try:
        brand = "Honda"
        name = bike.find_element(By.CLASS_NAME, "nameAndColor").text.strip()
        price_text = bike.get_attribute("data-price_from")
        price = re.sub(r"[^\d]", "", price_text)
        url = bike.find_element(By.TAG_NAME, "a").get_attribute("href")

        data.append([brand, name, price, url])

    except Exception as e:
        print(f"Lỗi khi lấy dữ liệu: {e}")

driver.quit()

df = pd.DataFrame(data, columns=["Thương hiệu", " Model", " Giá", " Link"])
df.to_csv("honda_motorcycles.csv", index=False, encoding="utf-8-sig")

print("Dữ liệu đã được lưu vào honda_motorcycles.csv")