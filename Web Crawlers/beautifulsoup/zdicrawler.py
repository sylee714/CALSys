# from _typeshed import NoneType
from os import write
import requests
# import libraries
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from enum import Enum


# Tags that need to be removed from the descriptions
remove_tags = ["<br/>", "<p>", "</p>"]

# Returns the name of a row when extracting information of a specific CVE.
def get_row_name(row):
    row_name = row.find_all('td')[0]
    return str(row_name.contents[0])

# Method that extracts the cve-id.
# Returns False, if there is no cve-id.
def extract_cve_id(row):
    row_tds = row.find_all('td')
    if row_tds[1].a is None:
        return False
    else:
        print("CVE-ID: ", str(row_tds[1].a.contents[0]))
        return str(row_tds[1].a.contents[0])
    
# Method that extracts the severity score of a cve.
def extract_severity_score(row):
    row_tds = row.find_all('td')

    # Get the score
    ss_str = str(row_tds[1].contents[0])

    # Remove empty spaces
    ss_str = ss_str.strip()

    # Remove the comma
    ss_str = ss_str.replace(",", "")

    print("Severity Score: ", ss_str)
    return ss_str

# Method that extracts the description of a cve.
def extract_description(row):
    description = row.find_all('td')[1].find_all('p')
    description_str = ""

    # Remove unnecessary tags
    for line in description:
        line = str(line)
        for tag in remove_tags:
            line = line.replace(tag, "")
        description_str = description_str + line
    
    # Remove white spaces at the front
    empty_space = True
    index = 0
    # Loop till a non-white space char
    while empty_space:
        if description_str[index] != " ":
            empty_space = False
        else:
            index += 1

    description_str = description_str[index:]

    print("Descriptions: ", description_str)
    return description_str


# Method thta extracts the zdi published date of a cve.
def extract_published_date(row):
    target_date = "Coordinated public release of advisory"
    date_list = row.find_all('td')[1].find_all('li')
    published_date = ""

    for date in date_list:
        date_str = str(date.contents[0])
        if target_date in date_str:
            # YYYY-MM-DD format
            published_date = date_str[:10]
            break

    print("Published Date: ", published_date)
    return published_date
    

# Method that extracts the table and gets each cve's hyperlink
def extract_cve_hyperlinks(web_driver):
    # Get the table that contains a list of vulnerabilities
    table = web_driver.find_element(By.ID, "publishedAdvisories")

    # Get the body of the table
    zdi_table_body = table.find_element(By.TAG_NAME, 'tbody')

    # Get all the rows
    zdi_table_body_rows = zdi_table_body.find_elements(By.TAG_NAME, 'tr')

    cve_hyperlinks = []
    # Go thru each row and go to each link
    for row in zdi_table_body_rows:
        tds = row.find_elements(By.TAG_NAME, 'td')
        cve_url = tds[6].find_element(By.TAG_NAME, 'a').get_attribute("href")
        cve_hyperlinks.append(cve_url)

    return cve_hyperlinks

# specify the url
urlpage = 'https://www.zerodayinitiative.com/advisories/published/' 
driver = webdriver.Firefox()

# get web-page
driver.get(urlpage)

# ----------------------------------
# Get All Year Options
# select_year_element = driver.find_element(By.ID, "select-year")
# select_year = Select(select_year_element)
# year_options = select_year.options
# ----------------------------------

# Only get CVEs from 2015-2017
year_options = ['2015', '2016', '2017']

# Initialize the lists
cve_ids = []
dates = []
severity_scores = []
descriptions = []

# Go thru each year 
for year in year_options:
    print("Extracting " + year + " Data...")
    # Get the select element and change the year
    select_year_element = driver.find_element(By.ID, "select-year")
    select_year = Select(select_year_element)
    select_year.select_by_value(year)

    # execute script to scroll down the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);\
    var lenOfPage=document.body.scrollHeight;return lenOfPage;")

    # Get the table that contains a list of vulnerabilities
    table = driver.find_element(By.ID, "publishedAdvisories")

    # Get the body of the table
    zdi_table_body = table.find_element(By.TAG_NAME, 'tbody')

    # Get all the rows
    zdi_table_body_rows = zdi_table_body.find_elements(By.TAG_NAME, 'tr')
    cve_hyperlinks = []

    # Sleep for 5sec to load the page
    time.sleep(5)

    # Go thru each row of the table and go to each link
    for row in zdi_table_body_rows:
        # Find and get the hyperlink
        tds = row.find_elements(By.TAG_NAME, 'td')
        cve_url = tds[6].find_element(By.TAG_NAME, 'a').get_attribute("href")

        # Get the cve page
        page = requests.get(cve_url)
        soup = BeautifulSoup(page.content, 'html.parser')

        # Extract the info of the cve
        # cve_id_exist = True
        for row in soup.find_all('tr'):
            # CVE ID
            if get_row_name(row) == "CVE ID":
                cve_id = extract_cve_id(row)
                if cve_id:
                    cve_ids.append(cve_id)
                    # cve_id_exist = True
                else:
                    # cve_id_exist = False
                    print("No CVE-ID")
                    break
            # CVSS SCORE
            elif get_row_name(row) == "CVSS SCORE":
                severity_scores.append(extract_severity_score(row))
            # VULNERABILITY DETAILS
            elif get_row_name(row) == "VULNERABILITY DETAILS":
                descriptions.append(extract_description(row))
            # DISCLOSURE TIMELINE
            elif get_row_name(row) == "DISCLOSURE TIMELINE":
                dates.append(extract_published_date(row))
        print("-----------------------------------")
    print("-------------------------------------------------------------")

# Turn the extrated data into pandas
zdi_data = pd.DataFrame({
    "CVE-ID": cve_ids,
    "ZDI Published Date": dates,
    "Severity Score": severity_scores,
    "Description": descriptions
})

# Write to a file
zdi_data.to_csv("zdi_samples.csv", index=False)

driver.quit()