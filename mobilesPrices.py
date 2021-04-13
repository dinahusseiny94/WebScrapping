import os
import re
import sys
import time
from telnetlib import EC

import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from urllib3.util import wait


def parsePage(browserDrive, start_page, scrollPages, scrollStep):
    browserDrive.get(start_page)
    time.sleep(10)
    pageDF = {}
    pagesCount = 1
    post_elems = []
    post_elems_prices = []
    if scrollPages == 'No More Products':
        while browser.find_element_by_tag_name('div'):
            scrollCommand = "window.scrollBy(0," + str(scrollStep) + ")"
            browserDrive.execute_script(scrollCommand)
            time.sleep(2)
            endText = browser.find_element_by_tag_name('div').text
            if scrollPages in endText:
                break
            else:
                print('Parsing Mobile Shop scroll no.' + str(pagesCount))
                pagesCount = pagesCount+1
                continue
    else:
        for i in range(scrollPages):
            scrollCommand = "window.scrollBy(0," + str(scrollStep) + ")"
            browserDrive.execute_script(scrollCommand)
            time.sleep(2)
            post_elems = browserDrive.find_elements_by_class_name("itemTitle")
            post_elems_prices = browserDrive.find_elements_by_class_name("itemPrice")
            print("scrollPage"+str(i))
    page = browserDrive.find_element_by_tag_name('body')
    bodyText = page.text
    buttonList = browser.find_elements_by_link_text("Next")
    nextButton = [elem.get_attribute('href') for elem in buttonList]
    for index, word in enumerate(bodyText):
        if word == '…':
            pagesCount = bodyText[index + 1]
    pageDF['productNames'] = post_elems
    pageDF['productPrices'] = post_elems_prices
    pageDF['bodyText'] = bodyText
    pageDF['pagesCount'] = pagesCount
    pageDF['nextButton'] = nextButton
    return pageDF


def parseSouq(browserDrive, url,mobileName, mobilePrice, mobileOrder, mobileURL):
    print('Page parsing...'+url)
    pageContent = parsePage(browserDrive, url, 20, 1000)
    productNames = pageContent['productNames']
    productPrices = pageContent['productPrices']
    nextButton = pageContent['nextButton']

    # Last page indication
    if len(productNames) < 60:
        nextButton = None

    for productName in pageContent['productNames']:
        postName = productName.text.strip()
        postName = re.sub(r"[\n\t]*", "", postName)
        mobileName.append(postName)
        order = len(mobileName)
        mobileOrder.append(order)
        mobileURL.append('www.souq.com')

    for productPrice in productPrices:
        postPrice = productPrice.text.strip()
        postPrice = re.sub(r"[\n\t]*", "", postPrice)
        mobilePrice.append(postPrice)

    while nextButton is not None:
        print(nextButton)
        parseSouq(browserDrive,nextButton,mobileName,mobilePrice,mobileOrder,mobileURL)


def parseMobileShop(browserDrive,url, mobileName, mobilePrice, mobileOrder, mobileURL):
    pageContent = parsePage(browserDrive,url, 'No More Products', 1000)
    print('Page parsing...' + url)
    bodyText = pageContent['bodyText']
    bodyText = bodyText.split('\n')
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
                    mobileName.append(productName)
                    mobilePrice.append(productPrice)
                    order = len(mobileName)
                    mobileOrder.append(order)
                    mobileURL.append('www.mobileshop.com')


def parseEgyPrices(browserDrive,startURL, mobileName, mobilePrice, mobileOrder, mobileURL):
    pageContent = parsePage(browserDrive, startURL, 5, 500)
    pagesCount = pageContent['pagesCount']
    print(pagesCount)
    for x in range(1, int(pagesCount)+1, 1):
        url = "https://www.egprices.com/en/category/mobile-phones-tablets/mobile-phones?&page=" + str(x)
        print('Pages parsing...' + url)
        pageContent = parsePage(browserDrive,url, 5, 500)
        bodyText = pageContent['bodyText']
        bodyText = bodyText.split('\n')
        for index, word in enumerate(bodyText):
            if 'Sold By' in word:
                productName = bodyText[index - 1]
                productPrice = bodyText[index + 1]
                if productPrice == 'Colors:' or productPrice == 'From':
                    productPrice = bodyText[index + 2]
                if productPrice == 'From' or productPrice == 'Colors:':
                    productPrice = bodyText[index + 3]
                productName = re.sub(r"[\n\t]*", "", productName)
                mobileName.append(productName)
                productPrice = re.sub(r"[\n\t]*", "", productPrice)
                mobilePrice.append(productPrice)
                order = len(mobileName)
                mobileOrder.append(order)
                mobileURL.append('www.egprices.com')
            else:
                continue


if __name__ == '__main__':
    print('Processing...')
    browser = webdriver.Chrome('/Users/dinaelhusseiny/Downloads/chromedriver')
    name = []
    price = []
    Web_scrapper_order = []
    Web_scrapper_start_url = []

    # parseSouq(browser,"https://egypt.souq.com/eg-en/mobile-phone/l/?sortby=sr",name,price,Web_scrapper_order,Web_scrapper_start_url)
    # browser.quit()
    # print('Finished Souq')

    parseMobileShop(browser,'https://www.mobileshop.com.eg/shop/1',name,price,Web_scrapper_order,Web_scrapper_start_url)
    print('Finished Mobile Shop')

    #parseEgyPrices(browser,"https://www.egprices.com/en/category/mobile-phones-tablets/mobile-phones?&page=1",name,price,Web_scrapper_order,Web_scrapper_start_url)
    #browser.quit()
    # print('Finished Egy Prices')

    df = pd.DataFrame(
        {'Web-scrapper-order': Web_scrapper_order, 'Web-scrapper-start-url': Web_scrapper_start_url, 'name': name,
         'price': price})
    outputPath = '/Users/dinaelhusseiny/Desktop/WebScraping'
    export_file_path = outputPath + '/MobilesPrices.csv'
    df.to_csv(export_file_path, index=False, header=True, encoding="utf-8-sig")

    if sys.platform == "win32":
        os.startfile('/Users/dinaelhusseiny/Desktop/WebScraping')
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        os.subprocess.call([opener, outputPath])

    print("Done!")
