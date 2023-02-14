import requests, json
import csv
from bs4 import BeautifulSoup
import re

# Regular expression pattern to match 21 CFR codes
# cfr_code_regex = re.compile(r"21 CFR (Part \d+ )?\d+(\.[A-Za-z0-9]+)*")
cfr_code_regex = re.compile(r"21 CFR \d+.[A-Za-z0-9]+")

# URL of the FDA warning letter
warning_letter_url = "https://www.fda.gov//inspections-compliance-enforcement-and-criminal-investigations/warning-letters/mohawk-laboratories-division-nch-corporation-635780-01182023"

# Fetch the content of the warning letter
response = requests.get(warning_letter_url)
warning_letter = response.text

# Search for 21 CFR codes in the warning letter
cfr_codes = re.findall(cfr_code_regex, warning_letter)

# Save the extracted CFR codes to a CSV file
try:
    with open("warning_letter_data.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["CFR Violation"])
        writer.writerow([", ".join(code for code in cfr_codes)])
    print("CFR violations have been saved to warning_letter_data.csv.")
    
except Exception as e:
    print(f"An error occurred while saving the file: {e}")

