import pandas as pd 
import re
import matplotlib.pyplot as plt 

file_path = "/Users/jsurya/Law-Innovation/web-scraping/data/inner_joined_table.csv"

df = pd.read_csv(file_path,header=0)


search_term = input("Enter a search term: ")


matches = df[(df["Long Description"].str.contains(search_term, case=False)) | 
             (df["Short Description"].str.contains(search_term, case=False))]

cfr_codes = []
for code in matches["Act/CFR Number"]:
    codes = re.findall(r'21 CFR (\d+\.\d+\([a-z]\))', code)
    cfr_codes.extend(codes)

counts = {}
for code in cfr_codes:
    if code in counts:
        counts[code] += 1
    else:
        counts[code] = 1

labels = counts.keys()
sizes = counts.values()
plt.figure()
plt.pie(sizes, labels=labels, autopct='%1.1f%%')
plt.title("CFR Code Distribution")
plt.show()

#--------------------------------------------#
company_names = []
for name in matches["Program Area"]:
    if not pd.isna(name):
        company_names.append(name.strip())

company_counts = {}
for name in company_names:
    if name in company_counts:
        company_counts[name] += 1
    else:
        company_counts[name] = 1


company_labels = company_counts.keys()
company_sizes = company_counts.values()
plt.figure()
plt.pie(company_sizes, labels=company_labels, autopct='%1.1f%%')
plt.title("Program Area Distribution")
plt.show()
