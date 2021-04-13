import re
import time
from selenium import webdriver
import pandas as pd

name = []
price = []
Web_scrapper_order = []
Web_scrapper_start_url = []

browser = webdriver.Chrome('/Users/dinaelhusseiny/Downloads/chromedriver')


def parse_page(start_page):
    browser.get(start_page)
    time.sleep(20)
    for i in range(2000):
        browser.execute_script("window.scrollBy(0, 200)")
        time.sleep(1)

    page = browser.find_element_by_tag_name('body')
    bodyText = page.text
    bodyText = bodyText.split('\n')
    count = 1

    for index, word in enumerate(bodyText):
        if word.upper() == 'BUY NOW' and word.upper != 'ON SALE':
            if 'EGP' in bodyText[index + 2]:
                productName = bodyText[index + 1]
                productPrice = bodyText[index + 2]
                print(productName)
                print(productPrice)
                productName = re.sub(r"[\n\t]*", "", productName)
                productPrice = re.sub(r"[\n\t]*", "", productPrice)
                if productName != 'ON SALE':
                    name.append(productName)
                    price.append(productPrice)
                    Web_scrapper_order.append(count)
                    Web_scrapper_start_url.append('www.mobileshop.com')
                    count += 1


parse_page("https://www.mobileshop.com.eg/shop/1")

browser.quit()

df = pd.DataFrame(
    {'Web-scrapper-order': Web_scrapper_order, 'Web-scrapper-start-url': Web_scrapper_start_url, 'name': name,
     'price': price})

export_file_path = '/Users/dinaelhusseiny/Desktop/WebScraping/Mobiles_mobileshop.csv'
df.to_csv(export_file_path, index=False, header=True)

print(df)
