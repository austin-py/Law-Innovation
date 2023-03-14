import pandas as pd 

import pickle 
import lzma

inspection_letter_df = pd.read_excel(
    "data/inspectionletters.xlsx", sheet_name="Sheet1", engine='openpyxl', header=0)

warning_letter_df = pd.read_csv(
    "data/pre_processed_warning_letter_final_data.csv")


with lzma.open('data/inspectionletters.pickle','wb') as f:
    pickle.dump(inspection_letter_df, f)
with lzma.open('data/warningletters.pickle','wb') as f:
    pickle.dump(warning_letter_df, f)