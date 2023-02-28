import os 
import time

from flask import Flask, render_template, request, url_for, redirect
from company_stats import get_cfr_links

#from search.search import Search

app = Flask(__name__)
print(Flask(__name__))


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        company_name = request.form["search_term"]
        return redirect(url_for("cfr",company_name= company_name))
    # try:
    #     os.remove(os.path.expanduser('~/Downloads/search_term.txt'))
    # except:
    #     pass
    return render_template('index.html')


@app.route("/cfr<company_name>")
def cfr(company_name):
    data = get_cfr_links(company_name)
    company_name = company_name
    return render_template('cfr.html', data = data, company_name = company_name)
    

# @app.route('/result', methods = ['POST','GET'])
# def result():
#     time.sleep(6)
#     s = Search()
#     print(s.term)
#     s.execute_search()
#     if request.method == 'POST':
#         result = request.form
#         return render_template('result.html',result = result)

if __name__ == "__main__":
    # try:
    #     os.remove(os.path.expanduser('~/Downloads/search_term.txt'))
    # except:
    #     pass
    app.run(debug = True)
