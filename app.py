from flask import Flask, render_template, request, url_for, redirect,g
from classes.StatGrabber import StatGrabber
from classes.CompanyStats import CompanyStats
from classes.WarningLetterStats import WarningLetterStats
from classes.InspectionLetterStats import InspectionLetterStats
import pickle
import lzma
from dotenv import load_dotenv

load_dotenv()

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
            return redirect(url_for("display_stats", search_term = search_term))
        elif request.form["checkbox_clicked"] == "Company Name":
            company_name = request.form["search_term"]
            return redirect(url_for("inspection_timeline", company_name=company_name))
    return render_template('index.html')

@app.route("/term/<search_term>", methods = ["POST","GET"])
def display_stats(search_term):
    g.w = WarningLetterStats(search_term,warning_letter_df)
    g.i = InspectionLetterStats(search_term,inspection_letter_df)
    if request.method == "GET":
        keys1, values1 = g.w.to_array()
        keys2, values2 = g.i.to_array()
        keys = keys1 + keys2
        values = values1 + values2
        g.warning_data = g.w.to_chart()
        inspection_data = g.i.to_chart()
        percent_data = g.w.to_pie()
        return render_template("search_stats.html", search_term=search_term, warning_data=g.warning_data, inspection_data=inspection_data, percent_data = percent_data)
    elif request.method == "POST":
        g.warning_links = [d['URL: '] for d in g.w.letters]
        g.company_names = [d['Company Name'] for d in g.w.letters]
        # print(f"CFR CODE: {g.w.USC_Codes}")
        # print(f"Warning Letter URLS: {g.warning_links}")
        return render_template('warning_links.html',warning_links = g.warning_links, company_names = g.company_names)


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


@app.route('/redirect')
def redirect_to_another_page():
    return render_template('index.html')


@app.route('/warning_links', methods = ["POST","GET"])
def display_warning_letters():
    # Render the new page with the label
    return render_template('warning_links.html',warning_links = g.warning_links)

if __name__ == "__main__":
    app.run()
