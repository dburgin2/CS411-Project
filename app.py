from flask import Flask, redirect, url_for, request, render_template, jsonify
from bs4 import BeautifulSoup
from threading import Timer
from flask_socketio import SocketIO, emit

# import the other files
import sql_python as sql_py
from tickerCloud import ticker_cloud
from PieChartCode import tickerPopular, tickerPie

app = Flask(__name__)
app.config['DEBUG'] = True

# turn the flask app into a socketio app
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

# @app.route('/')
# def home():
#     return render_template("home_RADS.html", records=None)


@app.route('/', methods=['GET', 'POST'])
def get_forms():
    if request.method == 'POST':
        # Then get the data from the form
        data = request.form
        if data['btn'] == "SH":
            print("SH")
            return search(data["tag"])
        elif data['btn'] == "Generate Word Cloud":
            print("Generating Word Cloud...")
            print(data)
            return gen_graphs(data)
        elif data['btn'] == "SI":
            print("SI")
            return insert(data)
        elif data['btn'] == "Insert Stocks":
            print("inserting into stocks...")
            return in_stock(data)
        elif data["btn"] == "Predict the future":
            print("Magic making time")
            return predict_stock(data)
        elif data["btn"] == "SU":
            print("SU")
            new_ticker = data["ntick"]
            new_secure = data["nsecu"]
            old_ticker = data["otick"]
            return update(new_ticker, new_secure, old_ticker)
        elif data["btn"] == "Find matches":
            print("Finding matches...")
            return stock_match(data)
        elif data["btn"] == "SD":
            print("SD")
            return delete(data)
        print(request.form)


        # Otherwise this was a normal GET request
    else:
        return render_template('home_RADS.html',
                               records=None,
                               activeStock=sql_py.select_active_stocks())


def gen_graphs(data):
    print(data["gen_word_cloud"])
    ticker = data["gen_word_cloud"]

    # generate the pictures for the cloud
    ticker_cloud(ticker)
    tickerPie(ticker)
    file_name = "static/wordcloud_" + data["gen_word_cloud"] + ".png"
    print(sql_py.second_complex_query())
    return render_template("word_cloud.html",
                           records=None,
                           file=file_name,
                           activeStock= sql_py.select_active_stocks(),
                           topten=sql_py.top_ten_price(),
                           volstock=sql_py.second_complex_query())

def stock_match(data):
    price = data["pr"]
    sector = data["se"]
    vo = data["vo"]
    suggestions = sql_py.GetUserStocks(price, sector, vo)
    print(suggestions)
    return render_template("home_RADS.html",
                           suggest=suggestions,
                           records=None)
def predict_stock(data):
    date = data["date"]
    tab = sql_py.GetGOOGLPrediction(date)
    print(tab)
    return render_template("word_cloud.html",
                           records=None,
                           file=None,
                           activeStock=sql_py.select_active_stocks(),
                           topten=sql_py.top_ten_price(),
                           volstock=sql_py.second_complex_query(),
                           date=date,
                           price=tab[1])

def delete(data):
    ticker = data["del"]
    sql_py.delete_security(ticker)
    return render_template("home_RADS.html", records=None)

def insert(data):
    ticker = data["insert_tick"]
    security_name = data["insert_secu"]
    success = sql_py.insert_security(ticker, security_name)
    return render_template("home_RADS.html",
                           records=None
                           )

def in_stock(data):
    ticker = data["in_symbol"]
    date = data["in_date"]
    open = data["in_open"]
    high = data["in_high"]
    low = data["in_low"]
    close = data["in_close"]
    adj_close = data["in_adj_close"]
    vol = data["in_vol"]
    sql_py.insert_stocks(ticker, date, open, high, low, close, adj_close, vol)
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
        return render_template("home_RADS.html",
                               company=security_name,
                               ticker=ticker,
                               date=None,
                               records=None)
    elif success_sn == False:
        return render_template("home_RADS.html",
                               company=None,
                               ticker=ticker,
                               date=None,
                               records=None)
    elif success_stocks == False:
        return render_template("home_RADS.html",
                               company=None,
                               ticker=ticker,
                               date=None,
                               records=None)

    print("here")
    records = records[0][1:]
    date = records[0]
    records = [round(x,3) for x in records[1:]]
    return render_template("home_RADS.html", company=security_name, ticker=ticker, date=date, records=records)


def update(new_ticker, new_secure, old_ticker):
    print(new_secure,new_ticker)
    if new_secure == '':
        print("no secure")
        sql_py.update_ticker(new_ticker, old_ticker)
    elif new_ticker == '':
        print("no new ticker")
        sql_py.update_security_name(old_ticker, new_secure)
    else:
        print("all of them")
        sql_py.update_ticker(new_ticker, old_ticker)
        sql_py.update_security_name(new_ticker, new_secure)

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
