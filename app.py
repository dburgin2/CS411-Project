from flask import Flask, render_template, request
from bs4 import BeautifulSoup
from threading import Timer
import sql_python as sql_py

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home_RADS.html", records=None)

@app.route("/")
def insert():
    pass

@app.route('/', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        # Then get the data from the form
        company = request.form['tag']
        # Get the username/password associated with this tag
        records = sql_py.fin_search(company)
        assert company == records[0][0]
        records = records[0][1:]
        date = records[0]
        records = [round(x,3) for x in records[1:]]
        return render_template("home_RADS.html", company=company, date=date, records=records)

        # Otherwise this was a normal GET request
    else:
        return render_template('home_RADS.html')

@app.route('/update', methods=['GET', 'POST'])
def update():
    pass

@app.route("/")
def delete():
    pass

def snackbarpopup():
    # find the snackbar DIV
    soup = BeautifulSoup("home_RADS.html", "html.parser")
    x = soup.find(id="snackbar")

    # Add the "show" class to DIV
    x.className = "show"

    def rmSnacks(className):
        className = className.replace("show", "")
    # remove snackbar after time runs out
    time = Timer(5.0,rmSnacks, x.className)

    time.start()

if __name__ == '__main__':
    app.run()
