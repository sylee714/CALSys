# import libraries
import os.path
from os import write
import requests
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from enum import Enum

data = pd.read_csv("C:/Users/SYL/Desktop/CALSysLab/Code/Files/filtered_mitre_zdi_data_with_binary.csv")
save_path = 'C:/Users/SYL/Desktop/CALSysLab/Code/Files/NVD-html-files/'

# Specify the url
base_url = 'https://nvd.nist.gov/vuln/detail/CVE-' 
driver = webdriver.Firefox()

# Get web-page
# driver.get(urlpage)

# Max Timeout sec
timeout = 10
timesleep = 5

for index, row in data.iterrows():
    cve_id = row['CVE-ID'][4:] # Do not include 'cve-' 
    url = base_url + cve_id

    driver.get(url)

    try:
        # Wait till the search input element loads
        element_present = EC.presence_of_all_elements_located((By.ID, 'changeHistoryToggle'))
        WebDriverWait(driver, timeout).until(element_present)
        

    except:
        # Went over the timeout limit
        print("Timed out waiting for page to load")

    # Click the hyperlink to open the history change
    driver.find_element(By.ID, "changeHistoryToggle").click()

    # Get the source page
    pageSource = driver.page_source

    # Write the source page to a file
    complete_file_name = os.path.join(save_path, cve_id+".html")
    fileToWrite = open(complete_file_name, "w", encoding='utf-8')
    fileToWrite.write(pageSource)
    fileToWrite.close()
    print("Successfully downloaded CVE:", cve_id)

    time.sleep(timesleep)

