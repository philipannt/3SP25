import mysql.connector
import json

# Thiết lập kết nối đến MySQL
conn = mysql.connector.connect(
    host="localhost",  # Đổi thành địa chỉ máy chủ của bạn nếu cần
    user="root",  # Thay bằng user của MySQL
    password="1234@Bcd",  # Thay bằng password của MySQL
    database="proj_ady"  # Thay bằng tên database của bạn
)

cursor = conn.cursor()

try:
    # Đọc dữ liệu từ file JSON
    with open(r"E:/Python/3SP25/CHOTOT_motorcycles2.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    
    # Chuyển đổi JSON thành chuỗi
    json_string = json.dumps(data, separators=(',', ':'), ensure_ascii=False, indent=None).strip()
    
    # Gọi stored procedure với tham số JSON
    cursor.callproc("prcInsertDataOfBike", (json_string,))
    
    conn.commit()  # Commit giao dịch
    print("Inserted Data")

except mysql.connector.Error as err:
    print(f"Error: {err}")

except Exception as e:
    print(f"Something else failed: {e}")

finally:
    cursor.close()
    conn.close()
    print("Close Database Connection")