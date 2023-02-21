import os 

class Search_Term():
    def __init__(self) -> None:
        self.search_term = self.__read_term__()

    def __read_term__(self):
        with open(os.path.expanduser('~/Downloads/search_term.txt'), 'r') as f:
            term = f.read()
        return term 
    

st = Search_Term()
print(st.search_term)