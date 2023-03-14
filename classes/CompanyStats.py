import re

class CompanyStats():
    def __init__(self, df):
        self.data = df

    def get_cfr_links(self, company_name):
        company_df = self.data[self.data['Legal Name'] == company_name]
        company_df = company_df.groupby('Inspection ID', as_index=False).agg(list)
        company_df = company_df.to_dict('records')
        # print(company_df)
        ret = []

        for row in company_df:
            cfrs = row['Act/CFR Number']
            # print(cfrs)
            inspection_id = row['Inspection ID']
            date = row['Inspection End Date']
            description = row['Short Description']

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
            ret.append([inspection_id, cfrs, cfr_urls, date, description])
        return ret

    def get_inspection_info(self, inspection_id):
        inspection_letter_df = self.data[self.data['Inspection ID'] == int(
            inspection_id)]
        company_df = inspection_letter_df.groupby(
            'Inspection ID', as_index=False).agg(list)
        ret = []
        for column in company_df.columns:
            ret.append(company_df[column][0])
        return ret