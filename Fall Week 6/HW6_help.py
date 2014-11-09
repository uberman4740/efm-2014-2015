import Quandl
import time
import numpy as np

stock_list = ["AXP","BA","CAT","CSCO","CVX","DD","DIS","GE","GS","HD","IBM","INTC","JNJ","JPM","KO","MCD","MMM","MRK","MSFT","NKE","PFE","PG","T","TRV","UNH","UTX","VZ","WMT","XOM","INDEX_GSPC"]

def get_returns(ticker):
	mydata = Quandl.get("YAHOO/"+ticker.upper(),
		returns = "numpy", collapse = 'monthly',
		trim_start = "2007-01-01",trim_end="2013-12-31",
		authtoken="CrRFHc_UN4Y2xyrLVBN5")

	prices = []
	for i in range(0,len(mydata)):
		prices.append(mydata[i][6])
	monthly_returns=[]
	for i in range(0,len(prices)-1):
		monthly_returns.append(prices[i+1]/float(prices[i])-1)
	return monthly_returns