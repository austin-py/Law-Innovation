import pandas as pd
from nltk.corpus import stopwords
import string

warning_letter_df = pd.read_csv("web-scraping/data/pre_processed_warning_letter_final_data.csv")

print('read in data')

def process(text):
    # remove punct
    remove_punc = [c for c in text if c not in string.punctuation]

    # join punc together
    remove_punc = ''.join(remove_punc)

    # remove stop words
    words = [w.lower() for w in remove_punc.split() if w.lower()
             not in stopwords.words("english")]
    return set(words)


search_words = [] 
for index, row in warning_letter_df.iterrows():
    combo =  str(row['Processed Words']) + ' ' + str(row['Posted Date']) + ' ' + str(row['Letter Issue Date']) + ' ' + str(row['Company Name']) + ' ' + str(row['Issuing Office']) + ' ' + str(row['Subject']) + ' ' + str(row['Response Letter']) + ' ' + str(row['Closeout Letter']) + ' ' + str(row['URL: ']) + ' ' + str(row['CFR Codes: ']) + ' ' + str(row['USC Codes: ']) 
    search_words.append(combo)
    print('Processed index {}'.format(index))


warning_letter_df['search_words'] = search_words


warning_letter_df.to_csv('data/pre_processed_warning_letter_final_data.csv')