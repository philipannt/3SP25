import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Khởi tạo trình duyệt Chrome
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Chạy chế độ ẩn
driver = webdriver.Chrome(options=options)

# Truy cập trang Honda
url = "https://www.honda.com.vn/xe-may/san-pham"
driver.get(url)

# Khởi tạo WebDriverWait
wait = WebDriverWait(driver, 15)  # Timeout tối đa 15 giây

# 1. Chờ cho trang web tải xong
wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

# 2. Chờ phần tử chứa danh sách xe xuất hiện
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "category-item")))

# 3. Chờ class "price" xuất hiện trên trang
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "price")))

# Tìm tất cả các thẻ chứa thông tin xe máy
bike_elements = driver.find_elements(By.CLASS_NAME, "category-item")

# Danh sách chứa dữ liệu thu thập
data = []

# Lặp qua từng xe để lấy thông tin
for bike in bike_elements:
    try:
        brand = "Honda"
        name = bike.find_element(By.CLASS_NAME, "nameAndColor").text.strip()  # Lấy tên xe
        price = bike.find_element(By.CLASS_NAME, "price").text.strip()
        # price = re.sub(r"[^\d]", "", price)
        url = bike.find_element(By.TAG_NAME, "a").get_attribute("href")

        # Lưu vào danh sách
        data.append([brand, name, price, url])

    except Exception as e:
        print(f"Lỗi khi lấy dữ liệu: {e}")

# Đóng trình duyệt
driver.quit()

# Lưu dữ liệu vào file CSV
df = pd.DataFrame(data, columns=["Thương hiệu", " Model", " Giá", " Link"])
df.to_csv("honda_motorcycles.csv", index=False, encoding="utf-8-sig")

print("Dữ liệu đã được lưu vào honda_motorcycles.csv")