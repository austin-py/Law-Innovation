import time 
import os 
import regex as re 
import requests
import csv 

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import pandas as pd 
from text_grabber import Text_Grabber
from selenium.webdriver.common.by import By


class FDA_Web_Scraper():
    def __init__(self):
        self.driver = self.get_driver()
        self.links = []
        self.warning_letter_links = []
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
        elems = self.driver.find_element(By.CLASS_NAME,"form-control.input-sm")
        self.driver.execute_script("arguments[0].scrollIntoView();", elems)
        elem = Select(self.driver.find_element(By.CLASS_NAME,"form-control.input-sm"))
        elem.select_by_value('100')

    def gather_urls_for_letters(self):
        #For 30 iterations (approx 3000 letters) loop through grabbing all the URLS, clicking next, and doing it a
        for timer in range(30):
            time.sleep(2)
            html = self.driver.page_source
            time.sleep(2)

            #Find all links 
            soup = BeautifulSoup(html,'html.parser')
            for i in soup.find_all('td'):
              for j in i.find_all('a', href=True):
                self.links.append("https://www.fda.gov/"+j['href'])

            #Click next button 
            elems = self.driver.find_element(By.ID,"datatable_next")
            self.driver.execute_script("arguments[0].scrollIntoView();", elems)
            self.driver.execute_script("arguments[0].click();", elems)
            time.sleep(2)
        self.driver.close()

    def scrape_letter_urls(self):
        usc_patterns = [
            r"\b\d{1,2}\sU\.S\.C\.\s\d{1,5}\b",
        ]
        
        cfr_patterns = [
            r'CFR \d+\.\d+']

        for link in self.warning_letter_links: 
            # URL of the FDA warning letter

            # Fetch the content of the warning letter
            response = requests.get(link)
            warning_letter = response.text

            # Search for 21 CFR codes in the warning letter
            cfr_codes = [] 
            for pattern in cfr_patterns:
                cfr_codes += (re.findall(pattern, warning_letter))

            usc_codes = []
            for pattern in usc_patterns:
                 usc_codes += (re.findall(pattern, warning_letter))



            soup = BeautifulSoup(response.text,'html.parser')
            text_grabber = Text_Grabber(soup)
            text = text_grabber.grab_text()

            title = soup.find(class_ = "text-center content-title")
            header_text = title.find(string=True, recursive=False)

            self.codes.append({
                          "URL: ": link,
                          "CFR Codes: ":cfr_codes,
                          "USC Codes: ": usc_codes,
                          "Company Name": header_text,
                          "Letter Content": text,})
            

    def merge_with_exported_data(self):
        df = pd.read_csv("data/warning-letters-exported.csv", header = [0], on_bad_lines = 'skip', encoding = "UTF-8") 
        df2 = pd.DataFrame.from_dict(self.codes)
        df2['Company Name'] = df2['Company Name'].apply(lambda x: x.replace("\n", ""))
        df2['Company Name'] = df2['Company Name'].apply(lambda x: x.strip())
        df['Company Name'] = df['Company Name'].apply(lambda x: x.strip())


        merged = df.merge(df2, how='left', left_on='Company Name', right_on='Company Name') 
        merged.to_csv("data/warning_letter_final_data.csv")

        print("CFR violations have been saved to warning_letter_data.csv.")

    def scrape(self):
        self.setup_for_gather_urls_for_letters()
        self.gather_urls_for_letters()
        self.filter_links()
        print("Succesfully gathered ",len(self.warning_letter_links)  ," URLs to scrape\n")
        self.scrape_letter_urls()
        print("Sucesfully scraped all the letter urls\n")
        self.merge_with_exported_data()
        print("Succesfully merged the data into one csv\n")

    def filter_links(self):
        # Create an empty set to store unique link prefixes
        unique_link_prefixes = set()

        # Create a new list to store unique links
        warning_letter_links = []
        date_pattern = r'\d{8}$'


        # Loop through the links and filter out close out and response letters
        # Add unique links that have unique prefixes to the unique_links list
        for link in self.links:
            link_prefix = re.split(date_pattern, link)[0]
            # link_extension = re.findall(date_pattern, link)[0]
            if link_prefix not in unique_link_prefixes:
                unique_link_prefixes.add(link_prefix)
                warning_letter_links.append(link)

        self.warning_letter_links = warning_letter_links

