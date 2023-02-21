from search_term import Search_Term

class Search():
    def __init__(self) -> None:
        self.term = Search_Term().search_term
    
    def execute_search(self):
        pass


s = Search()
print(s.term)