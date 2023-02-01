from bs4 import BeautifulSoup


import requests
import csv


r = requests.get("https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/compliance-actions-and-activities/warning-letters")
while True: 
    soup = BeautifulSoup(r.text,'html.parser')
    links = []
    for i in soup.find_all('td', class_ = "priority-medium views-field views-field-company-name"):
      for j in i.find_all('a', href=True):
        links.append("https://www.fda.gov/"+j['href'])
        # print("Found the URL:", "https://www.fda.gov/"+j['href'])

# print(links)

for link in links: 
    temp = requests.get(link)
    soup_temp = BeautifulSoup(temp.text,'html.parser')
    print(soup.text)