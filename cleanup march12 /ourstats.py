import csv
from collections import Counter
import re
import matplotlib.pyplot as plt


# Function to extract the CFR codes from the CFR code column
def extract_cfr_codes(codes):
    extracted_codes = []
    for code in codes:
        cfr_numbers = re.findall(r'CFR \d+\.\d+', code)
        extracted_codes += cfr_numbers
    return extracted_codes


# Read in the CSV file and prompt the user for a search term
filename = input("Enter the name of the CSV file: ")
search_term = input("Enter a search term: ")

with open(filename, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    
    # Find all rows that contain the search term in the Letter content column
    matching_rows = [row for row in reader if search_term.lower() in row['Letter content'].lower()]
    
    # Extract the CFR codes from the CFR code column for all matching rows
    cfr_codes = []
    for row in matching_rows:
        codes = row['CFR codes'].split(';')
        extracted_codes = extract_cfr_codes(codes)
        cfr_codes += extracted_codes
    
    # Count the number of occurrences of each CFR code
    cfr_counts = dict(Counter(cfr_codes))
    
    # Create a bar graph of the CFR code counts
    labels = cfr_counts.keys()
    values = cfr_counts.values()
    plt.bar(labels, values)
    plt.xticks(rotation=90)
    plt.xlabel('CFR Code')
    plt.ylabel('Count')
    plt.show()
