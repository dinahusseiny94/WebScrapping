from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
import time

governorateName = []
policeStationName = []
postalOfficeName = []
postalCode = []
Web_scrapper_id = []

browser = webdriver.Chrome('/Users/dinaelhusseiny/Downloads/chromedriver')


def parse_page(start_page):
    browser.get(start_page)
    time.sleep(5)
    selectGov = Select(browser.find_element_by_id("ResidencyAddress_GovernorateId"))

    for govOption in selectGov.options:
        if govOption.text is not None and govOption.text != '--- اختر ---':
            govText = govOption.text
            selectGov.select_by_visible_text(govText)
            time.sleep(1)

            selectPoliceStations = Select(browser.find_element_by_id("ResidencyAddress_PoliceDepartmentId"))

            for policeStationOption in selectPoliceStations.options:
                if policeStationOption.text is not None and policeStationOption.text != '--- اختر ---':
                    policeStationText = policeStationOption.text
                    governorateName.append(govText)
                    policeStationName.append(policeStationText)
                    Web_scrapper_id.append(len(policeStationName))
                    print(len(policeStationName))
                    print(govText)
                    print(policeStationText)
                    # selectPoliceStations.select_by_visible_text(policeStationText)
                    # time.sleep(1)
                    # selectPostalCodes = Select(browser.find_element_by_id("ResidencyAddress_PostalCodeId"))


                    # for postalCodeOption in selectPostalCodes.options:
                    #     if postalCodeOption.text is not None and postalCodeOption.text != '--- اختر ---':
                    #         postalCodeText = postalCodeOption.text
                    #         selectPostalCodes.select_by_visible_text(postalCodeText)
                    #         postalCodeNumber = postalCodeOption.get_attribute("code")
                    #         postalOfficeName.append(postalCodeText)
                    #         postalCode.append(postalCodeNumber)
                    #
                    #
                    #         print(postalCodeText)
                    #         print(postalCodeNumber)
                    #         print(len(postalCode))


parse_page('https://publicservices.moi.gov.eg/CSR/CreateCSR?Email=ahmed.elamly78@gmail.com&Token'
           '=b40791a03f5ccf3ee688d0887489a70bd44db38e7c814b9e13b80127fbf59f64')
browser.quit()

df = pd.DataFrame(
    {'Web-scrapper-id': Web_scrapper_id,
     'Governorate Name': governorateName,
     'PoliceStation Name': policeStationName
     })

export_file_path = '/Users/dinaelhusseiny/Desktop/WebScraping/EgyptPoliceStations.csv'
df.to_csv(export_file_path, index=False, header=True, encoding="utf-8-sig")

print(df)
