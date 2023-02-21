import os 

class Search_Term():
    def __init__(self) -> None:
        self.search_term = self.read_term()

    def read_term(self):
        with open(os.path.expanduser('~/Downloads/search_term.txt'), 'r') as f:
            term = f.read()
        os.remove(os.path.expanduser('~/Downloads/search_term.txt'))
        return term 
    