import sys
import os
from os import path
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


def ticker_cloud(ticker):

	d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

	# Read the whole text.
	text = open(path.join(d, ticker +'tweets.txt')).read()

	# Generate a word cloud image
	stop_words = ["x80", "https", "co", "RT", "t", "xf0", "x9", "jpm", ticker] + list(STOPWORDS)
	wordcloud = WordCloud(max_font_size=40, stopwords = stop_words).generate(text)

	plt.switch_backend('Agg')
	fig = plt.figure()
	plt.imshow(wordcloud, interpolation="bilinear")
	plt.axis("off")
	# plt.show()
	fig.savefig("static/wordcloud.png", bbox_inches='tight')

	return


# list_companies = ["AAL", "AAPL", "AMD", "AZN", "BAC", "BBD", "CCL", "COTY", "CSCO", "C",
# 				  "DKNG", "ET", "FCEL", "FSR", "F", "GE", "GOLD", "INO", "INTC", "ITUB",
# 				  "JMIA", "LI", "MRNA", "MRO", "MSFT", "M", "NCLH", "NIO", "NKLA", "OXY",
# 				  "PBR", "PFE", "PLTR", "PLUG", "SPCE", "SRNE", "TSLA", "T", "UAL", "VALE",
# 				  "WFC", "WORK", "XOM", "XPEV"]
#
# for i in list_companies:
# 	ticker_cloud(i)

# ticker_cloud('AAL')

