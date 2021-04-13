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
    time.sleep(5)
    for i in range(5):
        browser.execute_script("window.scrollBy(0, 500)")
        time.sleep(1)
        carsDetails = browser.find_elements_by_class_name('col-12')
        for carDetails in carsDetails:
            carCard = carDetails.find_element_by_class_name('car-card')
            carEngines = carDetails.find_element_by_class_name('car-card__engines')
            carTitle = carCard.find_element_by_class_name('car-card__title').text
            carEnginesList = carEngines.find_elements_by_class_name('car-card__engines__body__list__item')
            for carEngine in carEnginesList:
                carEngineTitle = carTitle + '\t' + carEngine.find_element_by_class_name(
                    'car-card__engines__body__list__item__name').text
                carEnginePrice = carEngine.find_element_by_class_name('car-card__engines__body__list__item__price').text
                name.append(carEngineTitle)
                price.append(carEnginePrice)
                Web_scrapper_order.append(len(name))
                Web_scrapper_start_url.append('www.contactCars.com')


browser.get('https://www.contactcars.com/ar/cars/new')
for x in range(7):
    browser.execute_script("window.scrollBy(0, 100)")
    time.sleep(1)
post_elems = browser.find_elements_by_class_name("n-make-btn")
makeLinks = [elem.get_attribute('href') for elem in post_elems]
print(len(makeLinks))

for x in range(0, len(makeLinks)):
    print(makeLinks[x])
    parse_page(makeLinks[x])

browser.quit()

df = pd.DataFrame(
    {'Web-scrapper-order': Web_scrapper_order, 'Web-scrapper-start-url': Web_scrapper_start_url, 'name': name,
     'price': price})

export_file_path = '/Users/dinaelhusseiny/Desktop/WebScraping/Cars_contactCars.csv'
df.to_csv(export_file_path, index=False, header=True, encoding="utf-8-sig")

print(df)