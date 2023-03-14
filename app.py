from flask import Flask, render_template, request, url_for, redirect
from classes.StatGrabber import StatGrabber
from classes.CompanyStats import CompanyStats
from classes.WarningLetterStats import WarningLetterStats
from classes.InspectionLetterStats import InspectionLetterStats
import pickle
import lzma

app = Flask(__name__)
with lzma.open('data/inspectionletters.pickle','rb') as f:
    inspection_letter_df = pickle.load(f)
with lzma.open('data/warningletters.pickle','rb') as f:
    warning_letter_df = pickle.load(f)
inspection_letter_df.fillna(-1)
company_stats_df = inspection_letter_df.copy()
inspection_letter_df = inspection_letter_df.to_dict('records')

warning_letter_df.fillna(-1)
warning_letter_df = warning_letter_df.to_dict('records')

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        print(request.form["checkbox_clicked"])
        if request.form["checkbox_clicked"] == "Search Term":
            search_term = request.form["search_term"].lower().strip()
            w = WarningLetterStats(search_term,warning_letter_df)
            i = InspectionLetterStats(search_term,inspection_letter_df)
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
    stats = StatGrabber(company_name,inspection_letter_df,warning_letter_df)
    # We can pull WarningLetterStats from here too and display them somehow.  
    company_stats = CompanyStats(company_stats_df)
    if request.method == "POST":
        inspection = request.form["inspection_id"]
        data = company_stats.get_inspection_info(inspection)
        return render_template('inspection_info.html', data = data, inspection_id = inspection)
    elif request.method == "GET":
        data = company_stats.get_cfr_links(company_name)
        return render_template('timeline.html', data=data, company_name=company_name)


if __name__ == "__main__":
    app.run(debug=True)
