import os 
import time

from flask import Flask, render_template, request

from search.search import Search

app = Flask(__name__)
print(Flask(__name__))

@app.route("/")
def home():
    try:
        os.remove(os.path.expanduser('~/Downloads/search_term.txt'))
    except:
        pass
    return render_template('index.html')

@app.route('/result', methods = ['POST','GET'])
def result():
    time.sleep(6)
    s = Search()
    print(s.term)
    s.execute_search()
    if request.method == 'POST':
        result = request.form
        return render_template('result.html',result = result)

if __name__ == "__main__":
    try:
        os.remove(os.path.expanduser('~/Downloads/search_term.txt'))
    except:
        pass
    app.run()
