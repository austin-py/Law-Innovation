class WarningLetterStats():
    def __init__(self,search_term,data) -> None:
        self.month_strings = {'1': 'January', '2': 'February', '3': 'March', '4':'April','5':'May','6':'June',
                              '7':'July','8':'August','9':'September','10':'October','11':'November','12':'December'}
        self.search_term = search_term
        self.data = data
        self.letters = []

        self.num_letters = 0
        self.num_response = 0
        self.num_closeout = 0
        self.percent_response = 0
        self.percent_closeout = 0
        self.CFR_Codes = {}
        self.USC_Codes = {}
        self.dates = {}
        self.issuing_offices = {}
        self.subjects = {}

        self.company_names = set()

        self.PreProcess_Data()
    
    def PreProcess_Data(self) -> None:
        for row in self.data:
            if self.search_term in row["search_words"] or self.search_term in row["Company Name"]:  
                self.letters.append(row)
                self.num_letters +=1
                if type(row['Response Letter']) != float:
                    self.num_response +=1
                if type(row['Closeout Letter']) != float:
                    self.num_closeout +=1

                cfr_codes = row['CFR Codes: ']
                cfr_codes = cfr_codes.replace('[',"").replace(']',"").split(',')
                cfr_codes = [i.strip() for i in cfr_codes]
                # print(cfr_codes)
                if cfr_codes != ['']:
                    for code in cfr_codes:
                        self.CFR_Codes[code] = self.CFR_Codes.get(code,0) + 1

                usc_codes = row['USC Codes: ']
                usc_codes = usc_codes.replace('[',"").replace(']',"").split(',')
                usc_codes = [i.strip() for i in usc_codes]
                if usc_codes != ['']:
                    for code in usc_codes:
                        self.USC_Codes[code] = self.USC_Codes.get(code,0) + 1

                date = row['Posted Date']
                date = date.split('/')
                month = self.month_strings[date[0]]
                year = '20' + date[2]
                month_year = month + ' ' + year 
                #self.dates[month_year] = self.dates.get(month_year,0) + 1
                self.dates[int(year)] = self.dates.get(int(year),0) + 1


                issuing_office = row['Issuing Office']
                self.issuing_offices[issuing_office] = self.issuing_offices.get(issuing_office,0) + 1

                subjects = row['Subject'].split('/')
                for subject in subjects:
                    self.subjects[subject] = self.subjects.get(subject,0) + 1
                
            # print('Row Number {} Processed'.format(index))

        if self.num_letters == 0:
            self.percent_response = 0
            self.percent_closeout = 0
        else:
            self.percent_response = self.num_response / self.num_letters
            self.percent_closeout = self.num_closeout / self.num_letters

       
        new_dict = {}
        for key in self.CFR_Codes:
            new_key = key.replace("'", '')  # Remove internal quotation marks
            new_dict[new_key] = self.CFR_Codes[key]
        self.CFR_Codes = new_dict

        
        new_dict = {}
        for key in self.USC_Codes:
            new_key = key.replace("'", '')  # Remove internal quotation marks
            new_dict[new_key] = self.USC_Codes[key]
        self.USC_Codes = new_dict



    def __print__(self):
        print('\n')
        print("There are {} letters relating to {}.".format(self.num_letters,self.search_term))
        print("{} of those had a response letter, giving a {} response letter rate.".format(self.num_response,self.percent_response))
        print("{} of those had a closeout letter, giving a {} closeout letter rate.".format(self.num_closeout,self.percent_closeout))
        print("There are {} unique CFR Codes related to {}, and {} unique USC Codes.".format(len(self.CFR_Codes.keys()), self.search_term, len(self.USC_Codes.keys())))
        print("There are {} unique issuing offices related to your search term, and {} different subjects.".format(len(self.issuing_offices.keys()), len(self.subjects.keys())))
        print('\n')
    
    def to_array(self):
        self.CFR_Codes = dict(sorted(self.CFR_Codes.items(), key=lambda item: item[1], reverse=True))
        self.USC_Codes = dict(sorted(self.USC_Codes.items(), key=lambda item: item[1], reverse=True))
        self.dates = dict(sorted(self.dates.items(), key=lambda item: item[0]))
        self.issuing_offices = dict(sorted(self.issuing_offices.items(), key=lambda item: item[1], reverse=True))
        self.subjects = dict(sorted(self.subjects.items(), key=lambda item: item[1], reverse=True))
        
        values = [self.num_letters,self.num_response,self.num_closeout,self.percent_response,self.percent_closeout,self.CFR_Codes,self.USC_Codes
                ,self.dates,self.issuing_offices,self.subjects]
        keys = ["Number of Warning Letters", "Number of Responses from Warnings", "Number of Closeouts from Warnings", "Percentage of Reponses from FDA", "Percentage of Closeouts from FDA",
                "CFR Codes of Warning Letters", "USC Codes of Warning Letters", "Dates of Warning Letters", "Issuing Offices of Warning Letters", "Program Areas of Warning Letters"]

        return [keys,values]
    def to_chart(self):
        keys, values = self.to_array()
        ret = []
        for dict in values[5:]:
            labels = list(dict.keys())
            values = list(dict.values())
            ret.append([labels,values])
        return ret
    def to_pie(self):
        keys, values = self.to_array()
        print(f"KEYS:{keys[3]}")
        labels = list([keys[3], keys[4],"No Further Action from FDA"])
        values = list([values[3], values[4], 1 - (values[3] + values[4])])
        return [labels,values]


# import pandas as pd 
# 
# warning_letter_df = pd.read_csv(
    # "data/pre_processed_warning_letter_final_data.csv")
# 
# w = WarningLetterStats('listeria',warning_letter_df)
# w.__print__()