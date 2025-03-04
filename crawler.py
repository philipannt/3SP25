import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--allow-running-insecure-content")
options.add_argument("--disable-blink-features=AutomationControlled")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

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
        price = re.sub(r"[^\d]", "", price_text) if price_text else "N/A"
        url = bike.find_element(By.TAG_NAME, "a").get_attribute("href")

        data.append([brand, name, price, url])

    except Exception as e:
        print(f"Lỗi khi lấy dữ liệu: {e}")

driver.quit()

df = pd.DataFrame(data, columns=["Thương hiệu", "Model", "Giá", "Link"])
df.to_csv("honda.csv", index=False, encoding="utf-8-sig")

print("Done")