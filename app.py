import os 

from flask import Flask, render_template

app = Flask(__name__)
print(Flask(__name__))

@app.route("/")
def home():
    try:
        os.remove(os.path.expanduser('~/Downloads/search_term.txt'))
    except:
        pass
    return render_template('index.html')


if __name__ == "__main__":
    try:
        os.remove(os.path.expanduser('~/Downloads/search_term.txt'))
    except:
        pass
    app.run()
