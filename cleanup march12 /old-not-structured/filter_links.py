
from bs4 import BeautifulSoup
import regex as re 
import requests
import csv 
import pandas as pd 

#Find all links 
r = requests.get("https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/compliance-actions-and-activities/warning-letters")
soup = BeautifulSoup(r.text,'html.parser')
links = []
for i in soup.find_all('td'):
  for j in i.find_all('a', href=True):
    links.append("https://www.fda.gov/"+j['href'])



# Create an empty set to store unique link prefixes
unique_link_prefixes = set()

# Create a new list to store unique links
unique_links = []
date_pattern = r'\d{8}$'


# Loop through the links and filter out close out and response letters
# Add unique links that have unique prefixes to the unique_links list
for link in links:
    link_prefix = re.split(date_pattern, link)[0]
    link_extension = re.findall(date_pattern, link)[0]
    if link_prefix not in unique_link_prefixes:
        unique_link_prefixes.add(link_prefix)
        unique_links.append(link)

# Print the list of unique links
print(unique_links)