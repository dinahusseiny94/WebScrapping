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
    post_elems = []
    post_elems_prices = []
    browser.get(start_page)
    time.sleep(10)
    for i in range(20):
        browser.execute_script("window.scrollBy(0, 1000)")
        time.sleep(5)
        post_elems = browser.find_elements_by_class_name("itemTitle")
        post_elems_prices = browser.find_elements_by_class_name("itemPrice")
    buttonList = browser.find_elements_by_link_text("Next")
    if len(post_elems) < 60:
        nextButton = None
    else:
        nextButton = [elem.get_attribute('href') for elem in buttonList]
    for post in post_elems:
        postName = post.text.strip()
        order = len(name)+1
        postName = re.sub(r"[\n\t]*", "", postName)
        name.append(postName)
        Web_scrapper_order.append(order)
        Web_scrapper_start_url.append('www.souq.com')
    for post in post_elems_prices:
        postPrice = post.text.strip()
        postPrice = re.sub(r"[\n\t]*", "", postPrice)
        price.append(postPrice)
    return nextButton


button = parse_page("https://egypt.souq.com/eg-en/mobile-phone/l/?sortby=sr")
while button is not None:
    print(button[0])
    button = parse_page(button[0])
browser.quit()

df = pd.DataFrame(
    {'Web-scrapper-order': Web_scrapper_order, 'Web-scrapper-start-url': Web_scrapper_start_url, 'name': name,
     'price': price})

export_file_path = '/Users/dinaelhusseiny/Desktop/WebScraping/Mobiles_souq.csv'
df.to_csv(export_file_path, index=False, header=True)

print(df)
