import time

from selenium import webdriver
import pandas as pd

carModelNames = []
carEngineNames = []
carYearModel = []
carMakeNames = []
price = []
Web_scrapper_order = []
Web_scrapper_start_url = []
carMakeLinks = []

browser = webdriver.Chrome('/Users/dinaelhusseiny/Downloads/chromedriver')


def parse_page(start_page,carMakeLink):
    browser.get(start_page)
    time.sleep(5)
    pageText = browser.find_element_by_tag_name('body')
    pageYears = []
    bodyText = pageText.text
    bodyText = bodyText.split('\n')
    for word in bodyText:
        if len(word) == 4 and word.isnumeric():
            pageYears.append(word)
    pageYears = pageYears[1:]
    browser.execute_script("window.scrollBy(0, 500)")
    carsDetails = browser.find_elements_by_class_name('col-12')
    count = 0
    for carDetail in carsDetails:
        carCard = carDetail.find_element_by_class_name('car-card')
        carEngines = carDetail.find_element_by_class_name('car-card__engines')
        carTitle = carCard.find_element_by_class_name('car-card__title').text
        carTitle = carTitle.replace(carMakeLink,'')
        carEnginesList = carEngines.find_elements_by_class_name('car-card__engines__body__list__item')
        for carEngine in carEnginesList:
            carEngineName = carEngine.find_element_by_class_name('car-card__engines__body__list__item__name').text
            carEnginePrice = carEngine.find_element_by_class_name('car-card__engines__body__list__item__price').text
            carModelNames.append(carTitle)
            carEngineNames.append(carEngineName)
            carYearModel.append(pageYears[count])
            carMakeNames.append(carMakeLink)
            price.append(carEnginePrice)
            Web_scrapper_order.append(len(carEngineNames))
            Web_scrapper_start_url.append('www.contactCars.com')
        count += 1

browser.get('https://www.contactcars.com/ar/cars/new')
for x in range(7):
    browser.execute_script("window.scrollBy(0, 100)")
    time.sleep(1)
post_elems = browser.find_elements_by_class_name("n-make-btn")
carMakes = browser.find_elements_by_class_name("n-make-btn__name")
for carMake in carMakes:
    carMakeLinks.append(carMake.text)
makeLinks = [elem.get_attribute('href') for elem in post_elems]
print(len(makeLinks))

for x in range(0, len(makeLinks)):
    print(makeLinks[x])
    parse_page(makeLinks[x],carMakeLinks[x])

browser.quit()

df = pd.DataFrame(
    {'Web-scrapper-order': Web_scrapper_order, 'Web-scrapper-start-url': Web_scrapper_start_url, 'Car Make': carMakeNames,
     'Car Model': carModelNames,'Car Year': carYearModel,'Car Engine': carEngineNames,'price': price})

export_file_path = '/Users/dinaelhusseiny/Desktop/WebScraping/Cars_contactCars.csv'
df.to_csv(export_file_path, index=False, header=True, encoding="utf-8-sig")

print(df)