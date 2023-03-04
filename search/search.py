from search.search_term import Search_Term
import pandas as pd 
from nltk.corpus import stopwords
import string

import nltk 
nltk.download('stopwords')

class Search():
    def __init__(self) -> None:
        self.term = 'listeria' #input('Please enter a search term:  ')
        self.data = pd.read_csv('web-scraping/data/warning_letter_final_data.csv')
        self.related_letters = []
    
    def execute_search(self,parameter,text=True):
        for index, row in self.data.iterrows():
            if text:
                cleaned = self.clean_data(row[parameter])
            else:
                cleaned = row[parameter]
            if self.term in cleaned: 
                self.related_letters.append({'Index': index, 'URL': row['URL: '], 'CRF_Codes': row['CFR Codes: ']})


    def clean_data(self,text):
        # remove punct
        remove_punc = [c for c in text if c not in string.punctuation]

        # join punc together
        remove_punc = ''.join(remove_punc)

        # remove stop words
        list = [w.lower() for w in remove_punc.split() if w.lower() not in stopwords.words("english")]
        return set(list)

    def cluster(self):
        pass 

    def output_related(self): #TODO needs to dump as JSON 
        for letter in s.related_letters:
            print('\nLetter index {} with codes {} might be related \n'.format(letter['Index'],letter['URL']))

    def get_new_term(self):
        term = input('Please enter a search term:  ')
        self.term = term

"""
TODO:
- Clean Letter Content column for better searching (lowercase or somethin), remove stop words (Harita sent code)
- Add as much clustering as possible to search. 


So basically we are just processing the data we have as much as we can and presenting it, and maybe presenting it on subpages such
that you can click a graph section (like meat processing) and get more info on that specific category? 


Timelines......




Duntin brad street? 


How do the letters cluster?? Meat-packing, distribution, etc? 
Maybe we allow up to five search terms? 

"""

        


# s = Search()
# s.execute_search('Letter Content')
# s.output_related()


