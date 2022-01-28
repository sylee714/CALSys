# import libraries
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

# Specify the url
urlpage = 'https://nvd.nist.gov/vuln/detail/CVE-2017-0144' 
driver = webdriver.Firefox()

# Get web-page
driver.get(urlpage)

# Max Timeout sec
timeout = 10
timesleep = 5

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
print(type(pageSource))

# Write the source page to a file
fileToWrite = open("page_source.html", "w", encoding='utf-8')
fileToWrite.write(pageSource)
fileToWrite.close()

