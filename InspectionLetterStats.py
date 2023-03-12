class InspectionLetterStats():
    def __init__(self,search_term,data) -> None:
        self.search_term = search_term
        self.data = data
        self.letters = []

        self.num_letters = 0
        self.inspection_ids = set()
        self.fei_numbers = set()
        self.company_names = set()
        self.dates = {}
        self.program_areas = {}
        self.cfr_numbers = {} 

        self.PreProcess_Data()

    
    def PreProcess_Data(self) -> None:
        self.data.fillna(-1)
        for index,row in self.data.iterrows():
            if self.search_term in row["search_words"]:
                self.letters.append(row)
                self.num_letters +=1
                self.inspection_ids.add(row['Inspection ID'])
                self.fei_numbers.add(row['FEI Number'])
                self.company_names.add(row['Legal Name'])
                self.dates[row['Inspection End Date']] = self.dates.get(row['Inspection End Date'],0) + 1
                self.program_areas[row['Program Area']] = self.program_areas.get(row['Program Area'],0) + 1
                self.cfr_numers[row['Act/CFR Number']] = self.cfr_numbers.get(row['Act/CFR Number'],0 ) + 1 
            print('Row Number {} Processed'.format(index))


    def __print__(self):
        print('\n')
        print("There are {} letters relating to {}.".format(self.num_letters,self.search_term))
        print("There are {} unique CFR Codes related to {}, and {} unique USC Codes.".format(len(self.cfr_numbers.keys()), self.search_term))
        print('\n')
    
    def to_array(self):
        
        values = [self.num_letters,self.inspection_ids,self.fei_numbers,self.company_names,self.dates,self.program_areas,self.cfr_numbers]
        keys = ["num_letters_inspec", "inspection_ids", "fei_numbers", "company_names", "dates","program_areas","cfr_numbers"]


        return [keys,values]


import pandas as pd 
inspection_letter_df = pd.read_excel(
   "data/inspectionletters1.xlsx", sheet_name="Sheet1", header=0)
i = InspectionLetterStats('listeria',inspection_letter_df)
i.__print__()

