import os
import time

from flask import Flask, render_template, request, url_for, redirect
from company_stats import get_cfr_links, get_inspection_info
import pandas as pd

# from search.search import Search

app = Flask(__name__)
inspection_letter_df = pd.read_excel(
    "web-scraping/data/inspectionletters.xlsx", sheet_name="Sheet1", header=0)


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        company_name = request.form["search_term"]
        return redirect(url_for("cfr", company_name=company_name))
    # try:
    #     os.remove(os.path.expanduser('~/Downloads/search_term.txt'))
    # except:
    #     pass
    return render_template('index.html')


@app.route("/company/<company_name>", methods=["POST", "GET"])
def cfr(company_name):
    if request.method == "POST":
        inspection = request.form["inspection_id"]
        print(f"INPSECTION ID:{inspection}")
        return redirect(url_for("more_info", inspection=inspection))
    elif request.method == "GET":
        data = get_cfr_links(company_name, inspection_letter_df)
        company_name = company_name
        return render_template('timeline.html', data=data, company_name=company_name)


@app.route("/info/<inspection>")
def more_info(inspection):
    data = get_inspection_info(inspection, inspection_letter_df)
    return render_template('more_info.html', data=data, inspection_id=inspection)


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
    app.run(debug=True)
