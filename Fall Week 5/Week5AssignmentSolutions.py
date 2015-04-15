import csv
import time
import datetime
import matplotlib.pyplot as plt
import numpy as np


# Generating dictionaries for each asset. Note that you don't need to generate 
# dictionaries. You could also set up a list of lists for each, but a dictionary
# lets you organize data by the keys.

msft = {}
aapl = {}
glw = {}

# Takes in a filepath to a csv file and returns a dictionary with the dates,
# prices, and returns.
def loadassetinfo(filepath):
    with open(filepath, "rb") as csvfile:
        reader = csv.reader(csvfile)
        
        price = []
        date = []
        returns = [0]
        
        reader.next()
        
        for row in reader:  #Converts dates to a datetime object
            t = time.strptime(row[0], '%m/%d/%Y')
            date.append(datetime.datetime(t[0], t[1], t[2]))
            price.append(float(row[4]))
        
        date.reverse()  # Because quandl puts most recent data first
        price.reverse()
        
        for ii in range(1, len(price)):
            returns.append((price[ii] - price[ii - 1]) / price[ii - 1])

        a_dict = {'dates':date, 'prices':price, 'returns':returns}
    
    return a_dict

# Loads all of the assets.
msft = loadassetinfo("C:\Users\Allan Zhang\Dropbox\School Work\EFM\\2014-2015\Week 5\Week 5 Assignment Solutions\Week5AssignmentSolutions\GOOG-NASDAQ_MSFT.csv")
glw = loadassetinfo("C:\Users\Allan Zhang\Dropbox\School Work\EFM\\2014-2015\Week 5\Week 5 Assignment Solutions\Week5AssignmentSolutions\GOOG-NYSE_GLW.csv")
aapl = loadassetinfo("C:\Users\Allan Zhang\Dropbox\School Work\EFM\\2014-2015\Week 5\Week 5 Assignment Solutions\Week5AssignmentSolutions\GOOG-NASDAQ_AAPL.csv")

#===============================================================================
# 2.2: Basic functions that return the mean, std dev, and covariance of an asset
#===============================================================================

def a_mean(asset):
    s = 0
    
    for ret in asset['returns'][1:]:  # removes the first return, which is 0
        s = s + ret
    
    return s / (len(asset['returns']) - 1)  # Similarly need to subtract 1

def a_var(asset):
    s = 0
    
    mean = a_mean(asset)
    
    for ret in asset['returns'][1:]:  # removes the first return, which is 0
        s = s + (ret - mean) ** 2
    
    return (s / (len(asset['returns']) - 1))  # Similarly need to subtract 1

def a_cov(a1, a2):
    
    s = 0
    
    a1_mean = a_mean(a1)
    a2_mean = a_mean(a2)
    
    for ii in range(1, len(a1['returns'])):  # removes the first return, which is 0
        s = s + ((a1['returns'][ii] - a1_mean) * (a2['returns'][ii] - a2_mean))
    
    return s / (len(a1['returns']) - 1)  # Similarly need to subtract 1

#===============================================================================
# 2.3: More general functions. Now with dates!
#===============================================================================

# What this does is strip out all values in the asset dictionary that are greater or less than the desired date bounds, then returns the asset dictionary.
# To get the relevant functions above after, just plug the result of this function into the above functions.
def stripdates(asset, date_lower, date_upper):
    
    #ii = 0
    lower = 0
    upper = 0
    a = {}
    
    for ii in range(len(asset['dates'])):
        if asset['dates'][ii] <= date_lower:
            lower = ii+1
        elif asset['dates'][ii] >= date_upper:
            upper = ii+1
            break
    a['dates'] = asset['dates'][lower:upper]
    a['prices'] = asset['prices'][lower:upper]
    a['returns'] = asset['returns'][lower:upper]
    
    return a

#===============================================================================
# # 2.4: Crafting a portfolio
#===============================================================================
# a_w is a dictionary of weights as keys and the asset dictionaries as values
# Defaults included so I don't have to manually type those in when I want to do tests.
def portfolio(a_w, date_lower=datetime.datetime(2003, 1, 1), date_upper=datetime.datetime(2013, 12, 31)):  
     
    ret_var = {}
    a_w_s = {}
    
    for a in a_w.keys(): # Strip out all values outside of date range.
        a_w_s[a] = stripdates(a_w[a], date_lower, date_upper)
    
    ret = 0
    
    for a in a_w_s.keys(): # Finds the sum of weighted expected returns
        ret = ret + a_mean(a_w_s[a]) * a
        
    ret_var['return'] = ret
    
    var = 0
    
    for a in a_w_s.keys(): #Finds the portfolio variance
        for b in a_w_s.keys():
            var = var + (a_cov(a_w_s[a],a_w_s[b]) * a * b)
    
    ret_var['variance'] = var
    
    return ret_var

#===============================================================================
# 
# NOTE
# The below functions that involve plotting will not show the graph. You will need to show it with plt.show() after running the function
#===============================================================================


#===============================================================================
# # 2.5: Plotting the Efficient Frontier
#===============================================================================
def twoassetfrontier(a1, a2, date_lower=datetime.datetime(2003, 1, 1), date_upper=datetime.datetime(2013, 12, 31)):  # Takes in 2 assets and lower/upper dates
    ret = []
    stddev = []
    a_w = {}
    
    for ii in np.arange(0, 1, .01): # Decided to just use numpy to make things easier on me. Could have also just iterated from 1 to 20 and divided the result by 20.
        a_w[ii] = a1 # Key = weight, value = asset
        a_w[1 - ii] = a2
        r = portfolio(a_w,date_lower,date_upper)['return']
        v = portfolio(a_w,date_lower,date_upper)['variance']**(.5)
        ret.append(r)
        stddev.append(v)
        a_w = {} #Resets the dictionary
    plt.scatter(stddev, ret)
    
#===============================================================================
# # 2.6: Efficient Frontier with More Assets
#===============================================================================
def threeassetfrontier(a1, a2, a3, date_lower=datetime.datetime(2003, 1, 1), date_upper=datetime.datetime(2013, 12, 31)):  # Takes in 3 assets and lower/upper dates
    ret = []
    stddev = []
    a_w = {}
    
    for ii in np.arange(0, 1, .01):
        for jj in np.arange(0, 1, .01):
            if ii + jj <= 1: #Ensures that you only get portfolios with valid asset weights
                a_w[ii] = a1
                a_w[jj] = a2
                a_w[1 - ii - jj] = a3
                ret.append(portfolio(a_w, date_lower, date_upper)['return'])
                stddev.append(portfolio(a_w, date_lower, date_upper)['variance']**(.5))
            a_w = {} #Resets the dictionary
    plt.scatter(stddev, ret)
    
#===============================================================================
# 2.7: Risk Free Rate and Sharpe Ratio
#===============================================================================

# Loading the Treasury CSV data.
with open("C:\Users\Allan Zhang\Dropbox\School Work\EFM\\2014-2015\Week 5\Week 5 Assignment Solutions\Week5AssignmentSolutions\WREN-W9.csv", "rb") as csvfile:
    reader = csv.reader(csvfile)
    
    date = []
    returns = [0]
    
    reader.next() #Skip Headers
    
    for row in reader:  #Converts dates to a datetime object
        t = time.strptime(row[0], '%m/%d/%Y')
        date.append(datetime.datetime(t[0], t[1], t[2]))
        returns.append(float(row[1])/100) #Quandl gives you percentage, so divide by 100 to make it comparable
    
    date.reverse()  # Because quandl puts most recent data first
    returns.reverse()

    treasury = {'dates':date, 'returns':returns}

#Finds the sharpe ratio for a given portfolio. For a single asset, just give it a portfolio with a single asset with a weight of 1.
#Takes same inputs as the portfolio function.
#If you wanted to be extra cool, you could even do away with all of this dictionary stuff and write up a portfolio class. Would probably be pretty useful here.
def sharperatio(a_w, date_lower=datetime.datetime(2003, 1, 1), date_upper=datetime.datetime(2013, 12, 31)):
    return ((portfolio(a_w,date_lower,date_upper)['return'] - a_mean(treasury))/(portfolio(a_w,date_lower,date_upper)['variance']**(.5)))

#To get sharpe ratios for each portfolio/asset, just plug them into the above function.

#===============================================================================
# 2.8: Plot the Capital Allocation Line
#===============================================================================

#Note that the a_w argument is totally unnecessary. Bad design on my part

def plotcal(a_w,date_lower=datetime.datetime(2003, 1, 1), date_upper=datetime.datetime(2013, 12, 31)):
    #Finds the largest sharpe ratio and plots that line. 
    maximum = 0
    for ii in np.arange(0, 1, .05):
        for jj in np.arange(0, 1, .05):
            if ii + jj <= 1:
                a_w[ii] = aapl
                a_w[jj] = msft
                a_w[1 - ii - jj] = glw
                if sharperatio(a_w,date_lower,date_upper) > maximum:
                    maximum = sharperatio(a_w,date_lower,date_upper)
            a_w = {}
            
    t = np.arange(0.,.2,0.05)
    plt.plot(t,a_mean(treasury) + maximum*t)

#===============================================================================
# 2.9: Variations over Time Frames
#===============================================================================
#Just uncomment the below

#===============================================================================
#threeassetfrontier(msft,glw,aapl,datetime.datetime(2003,1,1),datetime.datetime(2008,1,1))
#threeassetfrontier(msft,glw,aapl,datetime.datetime(2008,1,1),datetime.datetime(2013,12,31))
#plt.show()
#===============================================================================

#===============================================================================
# 2.10: Comparing Over Time Frames
#===============================================================================

def comparetimes():
    max_sharpe = 0
    max_weights = []
    a_w = {}
    
    #===========================================================================
    # msft_weight = []
    # sharpe_ratio = []
    #===========================================================================
    
    for ii in np.arange(0, 1, .05):
        for jj in np.arange(0, 1, .05):
            if ii + jj <= 1:
                a_w[ii] = aapl
                a_w[jj] = msft
                a_w[1-ii-jj] = glw
                
                sharpe = sharperatio(a_w,datetime.datetime(2003,1,1),datetime.datetime(2008,1,1))
                #===============================================================
                # msft_weight.append(jj) # For the microsoft lols
                # sharpe_ratio.append(sharpe)
                #===============================================================
                if sharpe > max_sharpe:
                    max_sharpe = sharpe
                    max_weights = [ii,jj,1-ii-jj]
                a_w = {}
    
    a_w = {max_weights[0]:aapl,max_weights[1]:msft,max_weights[2]:glw}
    print portfolio(a_w,datetime.datetime(2003,1,1),datetime.datetime(2008,1,1))
    print portfolio(a_w,datetime.datetime(2008,1,1),datetime.datetime(2013,1,1))
    print "In 2003-2008 the best Sharpe ratio was: ", max_sharpe, " for the asset weights: ", max_weights
    print "In 2008-2013, this portfolio had a Sharpe ratio of: ", sharperatio(a_w,datetime.datetime(2008,1,1),datetime.datetime(2013,12,31))
    print " for the asset weights: ", max_weights
    
    #===========================================================================
    # plt.scatter(msft_weight,sharpe_ratio) #For the microsoft lols
    # plt.show()
    #===========================================================================

#===============================================================================
# Post Function Section For Running Things
#===============================================================================

#twoassetfrontier(aapl,msft)
#a_w = {}
#plotcal(a_w)
#threeassetfrontier(msft, aapl, glw, datetime.datetime(2008,1,1), datetime.datetime(2013,12,31))
#plt.show()

#comparetimes()