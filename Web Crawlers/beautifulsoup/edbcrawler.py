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


# Read the original files
data = pd.read_csv("C:/Users/SYL/Desktop/CALSysLab/Code/Files/filtered_data.csv")
# data = pd.read_csv("C:/Users/SYL/Desktop/CALSysLab/Code/Files/negative_cases.csv")
# positive_cases = pd.read_csv("C:/Users/SYL/Desktop/CALSysLab/Code/Files/positive_cases.csv")

# Combine them
# data.append(positive_cases)

# Initialize lists
cve_ids = []
mitre_dates = []
cve_descriptions = []
og_labels = []
new_labels = []

number_of_changed_labels = 0

# Specify the url
urlpage = 'https://www.exploit-db.com/' 
driver = webdriver.Firefox()

# Get web-page
driver.get(urlpage)

# Max Timeout sec
timeout = 10
timesleep = 5

try:
    # Wait till the search input element loads
    element_present = EC.presence_of_all_elements_located((By.ID, 'exploits-table_filter'))
    WebDriverWait(driver, timeout).until(element_present)
    # Get the search input
    search_input_div_element = driver.find_element(By.ID, "exploits-table_filter")
    search_input_label_element = search_input_div_element.find_element(By.TAG_NAME, "label")
    search_input_element = search_input_label_element.find_element(By.TAG_NAME, "input")

except:
    # Went over the timeout limit
    print("Timed out waiting for page to load")

time.sleep(timesleep)

for index, row in data.iterrows():
    # Search a vulnerability
    cve_id = row['CVE-ID'][4:] # Do not include 'cve-' 
    search_input_element.send_keys(cve_id)

    # Sleep for a sec for the page to update
    time.sleep(timesleep)

    try:
        # Wait till the search input element loads
        element_present = EC.presence_of_all_elements_located((By.ID, 'exploits-table'))
        WebDriverWait(driver, timeout).until(element_present)
        exploits_table_element = driver.find_element(By.ID, 'exploits-table')
        exploits_table_body_element = exploits_table_element.find_element(By.TAG_NAME, 'tbody')
        exploits_table_row_element = exploits_table_body_element.find_element(By.TAG_NAME, 'tr')
        exploits_table_td_element = exploits_table_row_element.find_element(By.TAG_NAME, 'td')

        # Append data to the lists
        cve_id_str = str(row['CVE-ID'])
        mitre_date_str = str(row['MITRE Assign Date'])
        cve_description_str = str(row['CVE Description'])
        og_label_str = str(row['Label'])
        cve_ids.append(cve_id_str)
        mitre_dates.append(mitre_date_str)
        cve_descriptions.append(cve_description_str)
        og_labels.append(og_label_str)

        print("CVE-ID: ", cve_id_str)
        print("MITRE Date: ", mitre_date_str)
        print("Description: ", cve_description_str)
        print("OG Label: ", og_label_str)

        # Check if there is a PoC exploit
        if exploits_table_td_element.text == "No matching records found":
            if row['Label'] == 't':
                number_of_changed_labels += 1
                # print(cve_id + " | OG Label: " + row['Label'] + " | New Label: f")
            new_labels.append('f')
            print("New Label: f")
        else:
            if row['Label'] == 'f':
                number_of_changed_labels += 1
                # print(cve_id + " | OG Label: " + row['Label'] + " | New Label: t")
            new_labels.append('t')
            print("New Label: t")
        print("-------------------------------------------------")

        # Clear the search input
        search_input_element.clear()
    except:
        # Went over the timeout limit
        print("Timed out waiting for page to load")
        break

    # Sleep for 5sec to load the page
    time.sleep(timesleep)

print("Number of changed labels: ", number_of_changed_labels)

# Gives an error saying that the lists do not have the same length
# Turn the extrated data into pandas
new_data = pd.DataFrame({
    "CVE-ID": cve_ids,
    "MITRE Assign Date": mitre_dates,
    "CVE Description": cve_descriptions,
    "OG Label": og_labels,
    "New Label": new_labels
})

# Write to a file
new_data.to_csv("new_data.csv", index=False)

driver.quit()