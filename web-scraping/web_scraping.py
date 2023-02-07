import time 
import os 

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import regex as re 
import requests
import csv 
import pandas as pd 

links = [] 
path = os.getcwd() + '/utilities/chromedriver'
op = webdriver.ChromeOptions()
op.headless = False 
driver = webdriver.Chrome(path, options= op)
driver.maximize_window()

#Navigate to webpage 
driver.get("https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/compliance-actions-and-activities/warning-letters")

#Find, scroll-to, and change the number of letters visible from 10 to 100 
elems = driver.find_element_by_class_name("form-control.input-sm")
driver.execute_script("arguments[0].scrollIntoView();", elems)
elem = Select(driver.find_element_by_class_name("form-control.input-sm"))
elem.select_by_value('100')



links = []
#For 10 iterations (approx 1000 letters) loop through grabbing all the URLS, clicking next, and doing it again. 
for timer in range(1):
    time.sleep(2)
    html = driver.page_source
    time.sleep(2)

    #Find all links 
    soup = BeautifulSoup(html,'html.parser')
    for i in soup.find_all('td'):
      for j in i.find_all('a', href=True):
        links.append("https://www.fda.gov/"+j['href'])

    #Click next button 
    elems = driver.find_element_by_id("datatable_next")
    driver.execute_script("arguments[0].scrollIntoView();", elems)
    driver.execute_script("arguments[0].click();", elems)
    time.sleep(2)


for link in links:
    #Here we want to use the request library to get the text of each link 
    #Clean that text 
    #Save it to a file, or into the excel, or somewhere with a name so we can cross reference with excel sheet during later analysis. 
    pass 

cfr_code_regex = re.compile(r"21 CFR \d+.[A-Za-z0-9]+")
codes = []
for link in links: 
    # URL of the FDA warning letter

    # Fetch the content of the warning letter
    response = requests.get(link)
    warning_letter = response.text

    # Search for 21 CFR codes in the warning letter
    cfr_codes = re.findall(cfr_code_regex, warning_letter)

    soup = BeautifulSoup(response.text,'html.parser')
    
    title = soup.find(class_ = "text-center content-title")
    header_text = title.find(string=True, recursive=False)

    codes.append({
                  "URL: ": link,
                  "Warning Codes: ":cfr_codes,
                  "Company Name: ": header_text})
    
    
    
print(header_text)

fields = ["URL: ", "Warning Codes: "]

df = pd.read_csv("warning-letters.xlsx", header = [0], on_bad_lines = 'skip', encoding = "UTF-8") 
df2 = pd.DataFrame.from_dict(codes)
print(df)

merged = pd.merge(df, df2, on ='Company_ ')
# with open("warning_letter_data.csv", "w", newline="") as f:
    # writer = csv.DictWriter(f, fieldnames=fields)
    # writer.writeheader()
    # writer.writerows(codes)

    # print("CFR violations have been saved to warning_letter_data.csv.")