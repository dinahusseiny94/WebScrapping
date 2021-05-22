import math
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


def getCount(start_page):
    browser.get(start_page)
    try:
        carResults = browser.find_element_by_class_name('n-search-result__result')
        carCount = carResults.text
        carCount = carCount.replace('نتائج البحث (', '')
        carCount = carCount.replace(')', '')
        carCount = math.ceil(int(carCount) / 12)
    except:
        carCount = 0
    return carCount


def parse_page(start_page, carMakeLink):
    browser.get(start_page)
    time.sleep(5)
    carDetails = browser.find_elements_by_class_name('col-xl-4')
    count = 0

    for carDetail in carDetails:
        try:
            carCard = carDetail.find_element_by_class_name('n-engine-card__model')
            carTitle = carCard.find_element_by_xpath("span[@itemprop='name']").text
            carYear = carCard.find_element_by_xpath("span[@itemprop='productionDate']").text
            carTitle = carTitle.replace(carMakeLink, '')
        except:
            carTitle = ''
            carYear = ''

        try:
            carEngineCard = carDetail.find_element_by_class_name('n-engine-card__engine')
            carEngine = carEngineCard.text
        except:
            carEngine = ''

        try:
            carPriceCard = carDetail.find_element_by_class_name('n-engine-card__price')
            carPrice = carPriceCard.find_element_by_xpath("span[@itemprop='price']").text
        except:
            carPrice = ''

        carModelNames.append(carTitle)
        carEngineNames.append(carEngine)
        carYearModel.append(carYear)
        carMakeNames.append(carMakeLink)
        price.append(carPrice)
        Web_scrapper_order.append(len(carEngineNames))
        Web_scrapper_start_url.append('www.contactCars.com')
        count += 1

    return pagesCount


browser.get('https://www.contactcars.com/ar/cars/used')
for x in range(7):
    browser.execute_script("window.scrollBy(0, 100)")
    time.sleep(1)
post_elems = browser.find_elements_by_class_name("n-make-btn")
carMakes = browser.find_elements_by_class_name("n-make-btn__name")
for carMake in carMakes:
    carMakeLinks.append(carMake.text)
makeLinks = [elem.get_attribute('href') for elem in post_elems]

for x in range(0, len(makeLinks)):
    pagesCount = getCount(makeLinks[x])
    print(pagesCount)
    if pagesCount != 0:
        for y in range(1, pagesCount + 1):
            makepageUrl = makeLinks[x]
            print('carMakeURL:' + makepageUrl)
            parse_page(makepageUrl, carMakeLinks[x])
            oldPage = 'page=' + str(y)
            newPage = 'page=' + str(y + 1)
            makeLinks[x] = makeLinks[x].replace(oldPage, newPage)
    else:
        continue
browser.quit()

df = pd.DataFrame(
    {'Web-scrapper-order': Web_scrapper_order, 'Web-scrapper-start-url': Web_scrapper_start_url,
     'Car Make': carMakeNames,
     'Car Model': carModelNames, 'Car Year': carYearModel, 'Car Engine': carEngineNames, 'price': price})

export_file_path = '/Users/dinaelhusseiny/Desktop/WebScraping/Cars_contactCars_used.csv'
df.to_csv(export_file_path, index=False, header=True, encoding="utf-8-sig")

print(df)
