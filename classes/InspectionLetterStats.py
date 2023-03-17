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
        for row in self.data:
            if self.search_term in row["combo_words"] or self.search_term in row['Legal Name']:
                self.month_strings = {1: 'January', 2: 'February', 3: 'March', 4:'April',5:'May',6:'June',
                                        7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'}
                self.letters.append(row)
                self.num_letters +=1
                self.inspection_ids.add(row['Inspection ID'])
                self.fei_numbers.add(row['FEI Number'])
                self.company_names.add(row['Legal Name'])

                date = str(row['Inspection End Date']).split(' ')[0].split('-')
                month = self.month_strings[int(date[1])]
                year = date[0]
                month_year = month + ' ' + year
                #self.dates[month_year] = self.dates.get(month_year,0) + 1
                self.dates[year] = self.dates.get(year,0) + 1
                
                self.program_areas[row['Program Area']] = self.program_areas.get(row['Program Area'],0) + 1
                self.cfr_numbers[row['Act/CFR Number']] = self.cfr_numbers.get(row['Act/CFR Number'],0 ) + 1 
            # print('Row Number {} Processed'.format(index))


    def __print__(self):
        print('\n')
        print("There are {} letters relating to {}.".format(self.num_letters,self.search_term))
        print("There are {} unique CFR Codes related to {}".format(len(self.cfr_numbers.keys()), self.search_term))
        print('\n')
    
    def to_array(self):
        self.dates = dict(sorted(self.dates.items(), key=lambda item: item[0]))
        self.program_areas = dict(sorted(self.program_areas.items(), key=lambda item: item[1], reverse=True))
        self.cfr_numbers = dict(sorted(self.cfr_numbers.items(), key=lambda item: item[1], reverse=True))
        
        values = [self.num_letters,self.inspection_ids,self.fei_numbers,self.company_names,self.dates,self.program_areas,self.cfr_numbers]
        keys = ["Number of Inspection Letters", "Inspection Ids", "Inspection Fei Numbers", "Inspection Company Names", "Dates of Inspections","Program Areas Cited in Inspection","Cfr Codes Cited in Inspection"]


        return [keys,values]

    def to_chart(self):
        keys, values = self.to_array()
        ret = []
        for dict in values[4:]:
            labels = list(dict.keys())
            values = list(dict.values())
            ret.append([labels,values])
        return ret

    



# import pandas as pd 
# inspection_letter_df = pd.read_excel(
#    "data/inspectionletters1.xlsx", sheet_name="Sheet1", header=0)
# i = InspectionLetterStats('listeria',inspection_letter_df)
# i.__print__()
