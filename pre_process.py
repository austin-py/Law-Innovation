import pandas as pd
from nltk.corpus import stopwords
import string

warning_letter_df = pd.read_csv(
    "web-scraping/data/warning_letter_final_data.csv")


def process(text):
    # remove punct
    remove_punc = [c for c in text if c not in string.punctuation]

    # join punc together
    remove_punc = ''.join(remove_punc)

    # remove stop words
    words = [w.lower() for w in remove_punc.split() if w.lower()
             not in stopwords.words("english")]
    return set(words)


warning_letter_df.dropna(subset=['Letter Content'], inplace=True)
warning_letter_df["Processed Words"] = warning_letter_df['Letter Content'].apply(
    process)

warning_letter_df.to_csv("web-scraping/data/pre_processed_warning_letter_final_data.csv")
