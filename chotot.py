from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests

def scrape_chotot(url, pages):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
        }

        product_links = []
        product_list = []

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)

        for x in range(1, pages + 1):
            url_link = f"{url}?page={x}"
            r = requests.get(url_link, headers=headers)
            soup = BeautifulSoup(r.content, "lxml")
            products = soup.find_all("a", href=True, itemprop="item", class_="cebeqpz")

            for item in products:
                link = item['href']
                link = url + link if link.startswith("/") else link 
                product_links.append(link)

        for link in product_links:
            driver.get(link)
<<<<<<< Updated upstream
            
=======

>>>>>>> Stashed changes
            soup = BeautifulSoup(driver.page_source, "lxml")
            name = soup.find("title").text.strip()
            
            info_spans = soup.find_all("span", class_="bwq0cbs")
            info_list = [span.text.strip() for span in info_spans]

            year = info_list[0] if len(info_list) > 0 else "NONE"
            km = info_list[1] if len(info_list) > 1 else "NONE"
            nation = info_list[2] if len(info_list) > 2 else "NONE"
            location = info_list[3] if len(info_list) > 3 else "NONE"
            time = info_list[4] if len(info_list) > 4 else "NONE"
            
            price_tag = soup.find("b", class_="p26z2wb")
            price = price_tag.text.strip() if price_tag else "Price not available"

            price_elements = soup.find_all("div", class_="p1wx4fkc")
            price_min = price_elements[0].text.strip() if len(price_elements) > 0 else "Price not available"
            price_max = price_elements[1].text.strip() if len(price_elements) > 1 else "Price not available"

            product = {
                "name": name,
                "Year_of_manufacture": year,
                "Kilometers_driven": km,
                "Nationality": nation,
                "Location": location,
                "Listing_time": time,
                "price": price,
                "price_min": price_min,
                "price_max": price_max
            }

            product_list.append(product)
<<<<<<< Updated upstream
=======
            print(name)
        
        df = pd.DataFrame(product_list)
        df.to_json("CHOTOT.json", orient="records", force_ascii=False, indent=4)
        df.to_csv("CHOTOT.csv", index=False, encoding="utf-8-sig")
>>>>>>> Stashed changes
        
        driver.quit()
        
        return pd.DataFrame(product_list)

    except:
        print("Crawl error.")

scrape_chotot("https://xe.chotot.com/mua-ban-xe-may-da-nang", 100)