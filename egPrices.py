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
    pages_count = 0
    browser.get(start_page)
    time.sleep(10)
    for i in range(5):
        browser.execute_script("window.scrollBy(0, 500)")
        time.sleep(1)

    page = browser.find_element_by_tag_name('body')
    bodyText = page.text
    bodyText = bodyText.split('\n')
    for index, word in enumerate(bodyText):
        if word == '…':
            pages_count = bodyText[index + 1]
        if 'Sold By' in word:
            productName = bodyText[index - 1]
            productPrice = bodyText[index + 1]
            if productPrice == 'Colors:' or productPrice == 'From':
                productPrice = bodyText[index + 2]
            if productPrice == 'From' or productPrice == 'Colors:':
                productPrice = bodyText[index + 3]
            productName = re.sub(r"[\n\t]*", "", productName)
            name.append(productName)
            productPrice = re.sub(r"[\n\t]*", "", productPrice)
            price.append(productPrice)
            count = len(name) + 1
            Web_scrapper_order.append(count)
            Web_scrapper_start_url.append('www.egprices.com')
        else:
            continue
    return pages_count


pages_count = parse_page("https://www.egprices.com/en/category/mobile-phones-tablets/mobile-phones?&page=1")
print(pages_count)

for x in range(2, int(pages_count) + 1, 1):
    url = "https://www.egprices.com/en/category/mobile-phones-tablets/mobile-phones?&page=" + str(x)
    print(url)
    parse_page(url)

browser.quit()

df = pd.DataFrame(
    {'Web-scrapper-order': Web_scrapper_order, 'Web-scrapper-start-url': Web_scrapper_start_url, 'name': name,
     'price': price})


export_file_path = '/Users/dinaelhusseiny/Desktop/WebScraping/Mobiles_egprices.csv'
df.to_csv(export_file_path, index=False, header=True)

print(df)
