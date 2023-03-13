from flask import Flask, render_template, request, url_for, redirect
from classes.CompanyStats import CompanyStats
from classes.WarningLetterStats import WarningLetterStats
from classes.InspectionLetterStats import InspectionLetterStats
import pandas as pd

app = Flask(__name__)
inspection_letter_df = pd.read_excel(
    "data/inspectionletters.xlsx", sheet_name="Sheet1", engine='openpyxl', header=0)
warning_letter_df = pd.read_csv(
    "data/pre_processed_warning_letter_final_data.csv")

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        print(request.form["checkbox_clicked"])
        if request.form["checkbox_clicked"] == "Search Term":
            search_term = request.form["search_term"]
            w = WarningLetterStats(search_term,warning_letter_df)
            if w  == -1: 
                return render_template('index.html')
            i = InspectionLetterStats(search_term,inspection_letter_df)
            if i == -1: 
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
    stats = CompanyStats(inspection_letter_df)
    if request.method == "POST":
        inspection = request.form["inspection_id"]
        data = stats.get_inspection_info(inspection)
        return render_template('inspection_info.html', data = data, inspection_id = inspection)
    elif request.method == "GET":
        data = stats.get_cfr_links(company_name)
        return render_template('timeline.html', data=data, company_name=company_name)


if __name__ == "__main__":
    app.run(debug=True)
