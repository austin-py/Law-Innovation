import re

from bs4 import BeautifulSoup
class Text_Grabber():
    def __init__(self,soup):
        self.soup = soup
        self.data = ''
        self.all_text = ''
        

    def add_new_line(self,text, line_length):
        words = text.split()
        new_text = ""
        count = 0
        for word in words:
            new_text += word + " "
            count += 1
            if count % line_length == 0:
                new_text += "\n"
        return new_text

    def add_new(self,text, target_word, num_newlines):
        new_text = re.sub(target_word, '\n' * num_newlines + target_word, text)
        return new_text

    def grab_text(self):
        for data in self.soup.find_all("p"):
            text = data.get_text()
            self.all_text += (text)
            self.all_text += ("\n")

        line_length = 10
        new_text = self.add_new_line(self.all_text, line_length)
        f_text = self.add_new(new_text, "Dear", 3)
        final_text = self.add_new(f_text, "Sincerely", 3)
        # print(final_text) 

        #extracting title 
        # title = self.soup.find(class_ = "text-center content-title")
        # header_text = title.find(string=True, recursive=False)
        # print(header_text)
        return final_text