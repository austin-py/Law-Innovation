import pandas as pd 
from nltk.corpus import stopwords
import string

class WarningLetterStats():
    def __init__(self,search_term, data = None) -> None:
        self.search_term = search_term
        if not data:
            self.data = self.Load_Data()
        else:
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

        self.PreProcess_Data()

    def Load_Data(self) -> pd.DataFrame:
        df = pd.read_csv('web-scraping/data/warning_letter_final_data.csv')
        return df 
    
    def PreProcess_Data(self) -> None:
        self.data.fillna(-1)
        for index,row in self.data.iterrows():
            cleaned_words = self.Clean_Data(row['Letter Content'])
            if self.search_term in cleaned_words:
                self.letters.append(row)

                self.num_letters +=1
                if type(row['Response Letter']) != float:
                    self.num_response +=1
                if type(row['Closeout Letter']) != float:
                    self.num_closeout +=1

                cfr_codes = row['CFR Codes: '][0]
                for code in cfr_codes:
                    self.CFR_Codes[code] = self.CFR_Codes.get(code,0) + 1

                usc_codes = row['USC Codes: '][0]
                for code in usc_codes:
                    self.USC_Codes[code] = self.USC_Codes.get(code,0) + 1

                date = row['Posted Date']
                self.dates[date] = self.dates.get(date,0) + 1

                issuing_office = row['Issuing Office']
                self.issuing_offices[issuing_office] = self.issuing_offices.get(issuing_office,0) + 1

                subjects = row['Subject'].split('/')
                for subject in subjects:
                    self.subjects[subject] = self.subjects.get(subject,0) + 1
                
            print('Row Number {} Processed'.format(index))

        self.percent_response = self.num_response / self.num_letters
        self.percent_closeout = self.num_closeout / self.num_letters
    
    def Clean_Data(self,text):
        # remove punct
        remove_punc = [c for c in text if c not in string.punctuation]

        # join punc together
        remove_punc = ''.join(remove_punc)

        # remove stop words
        list = [w.lower() for w in remove_punc.split() if w.lower() not in stopwords.words("english")]
        return set(list)

    def __print__(self):
        print('\n')
        print("There are {} letters relating to {}.".format(self.num_letters,self.search_term))
        print("{} of those had a response letter, giving a {} response letter rate.".format(self.num_response,self.percent_response))
        print("{} of those had a closeout letter, giving a {} closeout letter rate.".format(self.num_closeout,self.percent_closeout))
        print("There are {} unique CFR Codes related to {}, and {} unique USC Codes.".format(len(self.CFR_Codes.keys()), self.search_term, len(self.USC_Codes.keys())))
        print("There are {} unique issuing offices related to your search term, and {} different subjects.".format(len(self.issuing_offices.keys()), len(self.subjects.keys())))
        print('\n')

       
w = WarningLetterStats('listeria')
w.__print__()



# Do same for subset of inspection letters that overlap 

