from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time 


import os 

import requests
import csv


links = [] 
path = os.getcwd() + '/utilities/chromedriver'
op = webdriver.ChromeOptions()
op.headless = False 
driver = webdriver.Chrome(path, options= op)
driver.maximize_window()

driver.get("https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/compliance-actions-and-activities/warning-letters")

elems = driver.find_element_by_class_name("form-control.input-sm")
driver.execute_script("arguments[0].scrollIntoView();", elems)
print(elems)

elem = Select(driver.find_element_by_class_name("form-control.input-sm"))
elem.select_by_value('100')


time.sleep(2)
html = driver.page_source
time.sleep(2)


soup = BeautifulSoup(html,'html.parser')
links = []
for i in soup.find_all('td', class_ = "priority-medium views-field views-field-company-name"):
  for j in i.find_all('a', href=True):
    links.append("https://www.fda.gov/"+j['href'])
    print("Found the URL:", "https://www.fda.gov/"+j['href'])

print(len(links))

# for link in links: 
    # temp = requests.get(link)
    # soup_temp = BeautifulSoup(temp.text,'html.parser')
    # print(soup.text)