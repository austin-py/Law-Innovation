import time 
import os 
import regex as re 
import requests
import csv 

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import pandas as pd 

class FDA_Web_Scraper():
    def __init__(self):
        self.driver = self.get_driver()
        self.links = []
        self.codes = []

    def get_driver(self):
        path = os.getcwd() + '/utilities/chromedriver'
        op = webdriver.ChromeOptions()
        op.headless = False 
        driver = webdriver.Chrome(path, options= op)
        driver.maximize_window()
        return driver 

    def setup_for_gather_urls_for_letters(self):
        self.driver.get("https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/compliance-actions-and-activities/warning-letters")
        #Find, scroll-to, and change the number of letters visible from 10 to 100 
        elems = self.driver.find_element_by_class_name("form-control.input-sm")
        self.driver.execute_script("arguments[0].scrollIntoView();", elems)
        elem = Select(self.driver.find_element_by_class_name("form-control.input-sm"))
        elem.select_by_value('100')

    def gather_urls_for_letters(self):
        #For 10 iterations (approx 1000 letters) loop through grabbing all the URLS, clicking next, and doing it a
        for timer in range(1):
            time.sleep(2)
            html = self.driver.page_source
            time.sleep(2)

            #Find all links 
            soup = BeautifulSoup(html,'html.parser')
            for i in soup.find_all('td'):
              for j in i.find_all('a', href=True):
                self.links.append("https://www.fda.gov/"+j['href'])

            #Click next button 
            elems = self.driver.find_element_by_id("datatable_next")
            self.driver.execute_script("arguments[0].scrollIntoView();", elems)
            self.driver.execute_script("arguments[0].click();", elems)
            time.sleep(2)

    def scrape_letter_urls(self):
        cfr_code_regex = re.compile(r"21 CFR \d+.[A-Za-z0-9]+")
        for link in self.links: 
            # URL of the FDA warning letter

            # Fetch the content of the warning letter
            response = requests.get(link)
            warning_letter = response.text

            # Search for 21 CFR codes in the warning letter
            cfr_codes = re.findall(cfr_code_regex, warning_letter)

            soup = BeautifulSoup(response.text,'html.parser')

            title = soup.find(class_ = "text-center content-title")
            header_text = title.find(string=True, recursive=False)

            self.codes.append({
                          "URL: ": link,
                          "Warning Codes: ":cfr_codes,
                          "Company Name": header_text})

    def merge_with_exported_data(self):
        df = pd.read_csv("warning-letters-utf8.csv", header = [0], on_bad_lines = 'skip', encoding = "UTF-8") 
        df2 = pd.DataFrame.from_dict(codes)
        df2['Company Name'] = df2['Company Name'].apply(lambda x: x.replace("\n", ""))
        df2['Company Name'] = df2['Company Name'].apply(lambda x: x.strip())
        df['Company Name'] = df['Company Name'].apply(lambda x: x.strip())


        merged = df.merge(df2, how='left', left_on='Company Name', right_on='Company Name') 
        merged.to_csv("warning_letter_data.csv")

        print("CFR violations have been saved to warning_letter_data.csv.")

    def scrape(self):
        self.setup_for_gather_urls_for_letters()
        self.gather_urls_for_letters()
        print("Succesfully gathered all URLs to scrape")
        self.scrape_letter_urls()
        print("Sucesfully scraped all the letter urls")
        # self.merge_with_exported_data()
