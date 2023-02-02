import time 
import os 

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup

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
for timer in range(10):
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

print(len(links))