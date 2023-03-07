import os 
import time

from selenium import webdriver
from selenium.webdriver.support.ui import Select

path = os.getcwd() + '/utilities/chromedriver'
op = webdriver.ChromeOptions()
op.headless = False 
driver = webdriver.Chrome(path, options= op)
driver.maximize_window()

#Navigate to webpage 
driver.get("https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/compliance-actions-and-activities/warning-letters")

time.sleep(2)
elems = driver.find_element_by_class_name("dt-buttons")
driver.execute_script("arguments[0].scrollIntoView();", elems)
elems.click()
time.sleep(40)

print('Done Sleeping')
try:
    elem = driver.find_element_by_id("vde-automatic-download")
except:
    elem = driver.find_element_by_id("vde-automatic-download")
driver.execute_script("arguments[0].scrollIntoView();", elems)
elem.click()







