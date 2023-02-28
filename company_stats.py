import pandas as pd
import matplotlib.pyplot as plt
import re


def get_cfr_links(company_name, inspection_letter_df):
    #inspection_letter_df = pd.read_excel("/Users/jsurya/Law-Innovation/web-scraping/data/inspection_letters.xlsx", sheet_name="Sheet1", header=0)

    #company_name = input("Enter a Company Name: ")

    company_df = inspection_letter_df[inspection_letter_df['Legal Name'] == company_name]
    company_df = company_df.groupby('Inspection ID', as_index=False).agg(list)
    print(company_df)
    ret = []

    for index, row in company_df.iterrows():
        cfrs = row['Act/CFR Number']
        print(cfrs)
        inspection_id = row['Inspection ID']
        date = row['Inspection End Date']
        cfr_urls = []
        for cfr in cfrs:
            title, part, subpart_section = cfr.split(" ")
            # Split the subpart/section into its section number and subpart (if applicable)
            subpart_section = subpart_section.strip("()")
            if "." in subpart_section:
                section_num, subpart_num = subpart_section.split(".")
                subpart_num = re.sub(r'\([a-zA-Z]+\)', '', subpart_num)
                subpart_num = re.sub(r'\D', '', subpart_num)
            else:
                section_num = subpart_section
                subpart_num = None

            if subpart_num:
                cfr_url = f"https://www.govinfo.gov/link/cfr/{title}/{section_num}?sectionnum={subpart_num}&link-type=pdf"
            else:
                cfr_url = f"https://www.govinfo.gov/link/cfr/{title}/{section_num}?&link-type=pdf"
            cfr_urls.append(cfr_url)
        ret.append([inspection_id, cfrs, cfr_urls,date])
    return ret
    


