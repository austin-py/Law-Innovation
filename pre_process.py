import pandas as pd
from nltk.corpus import stopwords
import string

inspection_letter_df = pd.read_excel( "web-scraping/data/inspectionletters.xlsx", sheet_name="Sheet1", header=0)


def process(text):
    # remove punct
    remove_punc = [c for c in text if c not in string.punctuation]

    # join punc together
    remove_punc = ''.join(remove_punc)

    # remove stop words
    words = [w.lower() for w in remove_punc.split() if w.lower()
             not in stopwords.words("english")]
    return set(words)

combo_words = []
for index, row in inspection_letter_df.iterrows():
    combo = str(row['Short Description']) + ' ' + str(row['Long Description'])
    processed = process(combo)
    combo_words.append(processed)
print('Processed Round 1')

inspection_letter_df['combo_words'] = combo_words

search_words = [] 
for index, row in inspection_letter_df.iterrows():
    combo = str(row['combo_words']) + ' ' + str(row['Inspection ID']) + ' ' + str(row['FEI Number']) + ' ' + str(row['Legal Name']) + ' ' + str(row['Program Area']) + ' ' + str(row['Act/CFR Number']) + ' ' + str(row['Inspection End Date'])
    search_words.append(processed)
print('Processed Round 2')


inspection_letter_df['search_words'] = search_words


inspection_letter_df.to_excel('inspectionletters1.xlsx')