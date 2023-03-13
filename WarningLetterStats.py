class WarningLetterStats():
    def __init__(self,search_term,data) -> None:
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

        t = self.PreProcess_Data()
        if t == -1 :
            return -1
    
    def PreProcess_Data(self) -> None:
        self.data.fillna(-1)
        for index,row in self.data.iterrows():
            if self.search_term in row["search_words"]:  
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
                self.dates[date] = self.dates.get(date,0) + 1

                issuing_office = row['Issuing Office']
                self.issuing_offices[issuing_office] = self.issuing_offices.get(issuing_office,0) + 1

                subjects = row['Subject'].split('/')
                for subject in subjects:
                    self.subjects[subject] = self.subjects.get(subject,0) + 1
                
            # print('Row Number {} Processed'.format(index))

        if self.num_letters == 0: return -1 
        self.percent_response = self.num_response / self.num_letters
        self.percent_closeout = self.num_closeout / self.num_letters
        return 1

    def __print__(self):
        print('\n')
        print("There are {} letters relating to {}.".format(self.num_letters,self.search_term))
        print("{} of those had a response letter, giving a {} response letter rate.".format(self.num_response,self.percent_response))
        print("{} of those had a closeout letter, giving a {} closeout letter rate.".format(self.num_closeout,self.percent_closeout))
        print("There are {} unique CFR Codes related to {}, and {} unique USC Codes.".format(len(self.CFR_Codes.keys()), self.search_term, len(self.USC_Codes.keys())))
        print("There are {} unique issuing offices related to your search term, and {} different subjects.".format(len(self.issuing_offices.keys()), len(self.subjects.keys())))
        print('\n')
    
    def to_array(self):
        
        values = [self.num_letters,self.num_response,self.num_closeout,self.percent_response,self.percent_closeout,self.CFR_Codes,self.USC_Codes
                ,self.dates,self.issuing_offices,self.subjects]
        keys = ["Number of Warning Letters", "Number of Responses from Warnings", "Number of Closeouts from Warnings", "Percentage of Reponses from FDA", "Percentage of Closeouts from FDA",
                "CFR Codes of Warning Letters", "USC Codes of Warning Letters", "Dates of Warning Letters", "Issuing Offices of Warning Letters", "Program Areas of Warning Letters"]

        return [keys,values]

# import pandas as pd 

# warning_letter_df = pd.read_csv(
    # "data/pre_processed_warning_letter_final_data1.csv")

# w = WarningLetterStats('listeria',warning_letter_df)
# w.__print__()