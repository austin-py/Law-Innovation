from flask import Flask, render_template, request, url_for, redirect
from company_stats import get_cfr_links, get_inspection_info
from WarningLetterStats import WarningLetterStats
from InspectionLetterStats import InspectionLetterStats
import pandas as pd

app = Flask(__name__)
inspection_letter_df = pd.read_excel(
    "web-scraping/data/inspectionletters.xlsx", sheet_name="Sheet1", header=0)
warning_letter_df = pd.read_csv(
    "web-scraping/data/pre_processed_warning_letter_final_data.csv")

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        print(request.form["checkbox_clicked"])
        if request.form["checkbox_clicked"] == "Search Term":
            search_term = request.form["search_term"]
            w = WarningLetterStats(search_term,warning_letter_df)
            if w.num_letters == 0: 
                return render_template('index.html')
            i = InspectionLetterStats(search_term,inspection_letter_df)
            if i.num_letters == 0: 
                return render_template('index.html')
            keys1, values1 = w.to_array()
            keys2, values2 = i.to_array()
            keys = keys1 + keys2
            values = values1 + values2
            return render_template("warning_stats.html", keys = keys, values = values)
        elif request.form["checkbox_clicked"] == "Company Name":
            company_name = request.form["search_term"]
            return redirect(url_for("inspection_timeline", company_name=company_name))
    return render_template('index.html')


@app.route("/company/<company_name>", methods=["POST", "GET"])
def inspection_timeline(company_name):
    if request.method == "POST":
        inspection = request.form["inspection_id"]
        return redirect(url_for("inspection_info", inspection=inspection))
    elif request.method == "GET":
        data = get_cfr_links(company_name, inspection_letter_df)
        return render_template('timeline.html', data=data, company_name=company_name)


@app.route("/info/<inspection>")
def inspection_info(inspection):
    data = get_inspection_info(inspection, inspection_letter_df)
    return render_template('inspection_info.html', data=data, inspection_id=inspection)


if __name__ == "__main__":
    app.run(debug=True)
