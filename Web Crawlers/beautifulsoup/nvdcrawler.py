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
from concurrent.futures import ThreadPoolExecutor

# https://medium.com/geekculture/introduction-to-selenium-and-python-multi-threading-module-aa5b1c4386cb

# data = pd.read_csv("C:/Users/SYL/Desktop/CALSysLab/Code/Files/filtered_mitre_zdi_data_with_binary.csv")
data = pd.read_csv("C:/Users/SYL/Desktop/CALSysLab/Code/Files/patched_cves.csv")
save_path = 'C:/Users/SYL/Desktop/CALSysLab/Code/Files/0Day-NVD-html-files/'
files_dir_path = "../../Files/"

# Specify the url
# base_url = 'https://nvd.nist.gov/vuln/detail/CVE-'
base_url = 'https://nvd.nist.gov/vuln/detail/'

# Max Timeout sec
timeout = 10
timesleep = 5

# Number of threads
num_of_workers = 4

# List of files
file_names = ["patched_cves_0.csv", "patched_cves_1.csv", "patched_cves_2.csv", "patched_cves_3.csv"]

def download_html(file_name, web_driver):

    data = pd.read_csv(files_dir_path + file_name)

    for index, row in data.iterrows():
        cve_id = row['CVE-ID']  # Do not include 'cve-'
        url = base_url + cve_id

        web_driver.get(url)

        try:
            # Wait till the search input element loads
            # element_present = EC.presence_of_all_elements_located((By.ID, 'changeHistoryToggle'))
            # WebDriverWait(driver, timeout).until(element_present)
            element_present = WebDriverWait(web_driver, timeout).until(
                EC.presence_of_element_located((By.ID, 'changeHistoryToggle'))
            )

        except Exception:
            # Went over the timeout limit
            print("Timed out waiting for page to load")

        # Click the hyperlink to open the history change
        web_driver.find_element(By.ID, "changeHistoryToggle").click()

        # Get the source page
        pageSource = web_driver.page_source

        # Write the source page to a file
        complete_file_name = os.path.join(save_path, cve_id + ".html")
        fileToWrite = open(complete_file_name, "w", encoding='utf-8')
        fileToWrite.write(pageSource)
        fileToWrite.close()
        print("Successfully downloaded:", cve_id)

        time.sleep(timesleep)


def setup_workers():

    drivers = [webdriver.Firefox() for i in range(len(file_names))]

    with ThreadPoolExecutor(max_workers=num_of_workers) as executor:
        executor.map(download_html, file_names, drivers)

    for driver in drivers:
        driver.quit()


driver = webdriver.Firefox()

for file in file_names:
    download_html(file, driver)

driver.quit()

