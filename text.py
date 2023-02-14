import requests, json
import csv
from bs4 import BeautifulSoup
import re
from urllib.request import urlopen

#define function to get data
def getdata(url):
    r = requests.get(url)
    return r.text

#practice url 
prac = "https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/warning-letters/liquivape-649189-02022023"

#getting data 
html_data = getdata(prac)
soup = BeautifulSoup(html_data, features = "html.parser")

#getting text from data 
data = ''
all_text = ''
for data in soup.find_all("p"):
    text = data.get_text()
    all_text += (text)
    all_text += ("\n")

#making each data only 10 lines 
def add_new_line(text, line_length):
    words = text.split()
    new_text = ""
    count = 0
    for word in words:
        new_text += word + " "
        count += 1
        if count % line_length == 0:
            new_text += "\n"
    return new_text

line_length = 10
new_text = add_new_line(all_text, line_length)

def add_new(text, target_word, num_newlines):
    new_text = re.sub(target_word, '\n' * num_newlines + target_word, text)
    return new_text

f_text = add_new(new_text, "Dear", 3)
final_text = add_new(f_text, "Sincerely", 3)
print(final_text) 

#extracting title 
title = soup.find(class_ = "text-center content-title")
header_text = title.find(string=True, recursive=False)
print(header_text)

#adding to csv file 
try:
    with open("warning-letter-text.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "Text From Letter"])
        writer.writerow([header_text, final_text])
    print("success")
except:
    print("error")

