from search_term import Search_Term
import pandas as pd 

class Search():
    def __init__(self) -> None:
        self.term = 'listeria' #Search_Term().search_term
        self.data = pd.read_csv('web-scraping/data/warning_letter_final_data.csv')
        self.related_letters = []
    
    def execute_search(self):
        for index, row in self.data.iterrows():
            if self.term in row['Letter Content']: #TODO need to clean up the text before searching. 
                self.related_letters.append({'Index': index, 'URL': row['URL: '], 'CRF_Codes': row['CFR Codes: ']})

        print("YAY search executed")

    def cluster(self):
        pass 

    def output_related(self): #TODO needs to dump as JSON 
        for letter in s.related_letters:
            print('\nLetter index {} with codes {} might be related \n'.format(letter['Index'],letter['URL']))

"""
TODO:
- Clean Letter Content column for better searching (lowercase or somethin), remove stop words (Harita sent code)
- Add as much clustering as possible to search. 


So basically we are just processing the data we have as much as we can and presenting it, and maybe presenting it on subpages such
that you can click a graph section (like meat processing) and get more info on that specific category? 


Timelines......







How do the letters cluster?? Meat-packing, distribution, etc? 
Maybe we allow up to five search terms? 

"""

        


s = Search()
s.execute_search()
s.output_related()


