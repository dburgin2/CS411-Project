import matplotlib.pyplot as plt
import pandas as pd


def tickerPopular(n):
    # Read in data, replace with correct path if necessary
    sentiments_df = pd.read_csv("TweetsWithSentiment.csv")

    # Return list of n most popular tickers
    return sentiments_df["ticker"].value_counts()[:n].index.tolist()

def tickerPie(ticker):
    # Read in data, replace with correct path if necessary
    sentiments_df = pd.read_csv("TweetsWithSentiment.csv")
    filtered_df = sentiments_df[sentiments_df["ticker"] == ticker]

    # Count number of positive and negative tweets
    nPositive = (filtered_df['sentiment'] == "positive").sum()
    nNegative = (filtered_df['sentiment'] == "negative").sum()

    # Specify labels and values for chart
    labels = "Positive", "Negative"
    counts = [nPositive, nNegative]

    # Create pie chart using specified labels and values
    plt.switch_backend('Agg')
    fig = plt.figure()
    plt.pie(counts, labels = labels, autopct = '%1.1f%%')
    plt.axis("equal")
    plt.title("Sentiment for " + ticker + " stock")
    # plt.show()
    print("here")
    fig.savefig("static/tickerPie.png", bbox_inches="tight")

tickerPie("AAPL")