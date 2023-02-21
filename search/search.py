from search_term import Search_Term
import pandas as pd 

class Search():
    def __init__(self) -> None:
        self.term = 'listeria' #Search_Term().search_term
        self.data = pd.read_csv('web-scraping/data/warning_letter_final_data.csv')
        self.related_letters = []
    
    def execute_search(self):
        for index, row in self.data.iterrows():
            if self.term in row['Letter Content']:
                self.related_letters.append({'Index': index, 'URL': row['URL: ']})
                
    def output_related(self):
        for letter in s.related_letters:
            print('\nLetter index {} with url {} might be related \n'.format(letter['Index'],letter['URL']))
        


s = Search()
s.execute_search()
s.output_related()


