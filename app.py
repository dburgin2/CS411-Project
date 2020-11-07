from flask import Flask, render_template, request
from bs4 import BeautifulSoup
from threading import Timer
import sql_python as sql_py

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home_RADS.html", records=None)


@app.route('/', methods=['GET', 'POST'])
def get_forms():
    if request.method == 'POST':
        # Then get the data from the form
        data = request.form
        if data['btn'] == "SH":
            print("SH")
            return search(data["tag"])
        elif data['btn'] == "SI":
            print("SI")
            return insert(data)
        elif data["btn"] == "SU":
            print("SU")
            new_ticker = data["ntick"]
            old_ticker = data["otick"]
            return update(new_ticker, old_ticker)
        elif data["btn"] == "SD":
            print("SD")
            return delete(data)
        print(request.form)


        # Otherwise this was a normal GET request
    else:
        return render_template('home_RADS.html')

def delete(data):
    ticker = data["del"]
    sql_py.delete_security(ticker)
    return render_template("home_RADS.html", records=None)

def insert(data):
    ticker = data["insert_tick"]
    security_name = data["insert_secu"]
    success = sql_py.insert_security(ticker, security_name)
    return render_template("home_RADS.html", records=None)

def search(ticker):
    # Then get the data from the form
    # Get the username/password associated with this tag
    if ticker == None:
        return render_template('home_RADS.html', records=None)
    success_stocks, records = sql_py.fin_search(ticker)
    success_sn, security_name = sql_py.get_security_name(ticker)
    # assert ticker == records
    if success_stocks == False and success_sn == True:
        return render_template("home_RADS.html", company=security_name, ticker=ticker, date=None, records=None)
    elif success_sn == False:
        return render_template("home_RADS.html", company=None, ticker=ticker, date=None, records=None)
    elif success_stocks == False:
        return render_template("home_RADS.html", company=None, ticker=ticker, date=None, records=None)

    print("here")
    records = records[0][1:]
    date = records[0]
    records = [round(x,3) for x in records[1:]]
    return render_template("home_RADS.html", company=security_name, ticker=ticker, date=date, records=records)


def update(new_ticker, old_ticker):
    sql_py.update_ticker(new_ticker, old_ticker)
    return render_template("home_RADS.html", records=None)

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
