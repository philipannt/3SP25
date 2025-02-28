import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--allow-running-insecure-content")
options.add_argument("--disable-features=NetworkService")

driver = webdriver.Chrome(options=options)

url = "https://xe.chotot.com/mua-ban-xe-may-quan-hai-chau-da-nang"
driver.get(url)

WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.AdItem_adItem__gDDQT")))

bike_elements = driver.find_elements(By.CSS_SELECTOR, "a.AdItem_adItem__gDDQT")

data = []

for bike in bike_elements:
    try:
        name = bike.find_element(By.CSS_SELECTOR, "h3.AdItem_adTitle__1MVoL").text
        price = bike.find_element(By.CSS_SELECTOR, "span.AdItem_price__VLhYG").text
        link = bike.get_attribute("href")

        driver.get(link)

        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.p1wx4fkc")))

        price_elements = driver.find_elements(By.CSS_SELECTOR, "div.p1wx4fkc")
        if len(price_elements) >= 2:
            min_price = price_elements[0].text
            max_price = price_elements[1].text
        else:
            min_price = "N/A"
            max_price = "N/A"

        driver.back()
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.AdItem_adItem__gDDQT")))

        data.append([name, price, min_price, max_price, link])

        print(f"Đã lấy: {name} - {price} ({min_price} - {max_price})")

    except Exception as e:
        print(f"Lỗi khi lấy dữ liệu: {e}")

driver.quit()

df = pd.DataFrame(data, columns=["Name", "Price", "Min Price", "Max Price", "Link"])
df.to_csv("chotot.csv", index=False, encoding="utf-8-sig")

print("done")