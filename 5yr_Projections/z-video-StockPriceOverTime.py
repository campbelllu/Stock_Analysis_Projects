#Gets highs, lows, closing price of stocks
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
from pandas_datareader import data
from pandas_datareader._utils import RemoteDataError

START_DATE = '2016-01-01'
END_DATE = str(dt.now().strftime('%Y-%m-%d'))

stock_1 = 'AAPL' #example from video
#data reader provides columns: Index(['High', 'Low', 'Open', 'Close', 'Volume', 'Adj Close'], dtype='object')
stock_2 = 'AMZN'

#Clean the data by
#filling in missing values of column provided
def clean_data(stock_data, col):
    weekdays = pd.date_range(start=START_DATE, end=END_DATE)
    clean_data = stock_data[col].reindex(weekdays)
    return clean_data.fillna(method='ffill')

#Get meaningful stats from these data
def get_stats(stock_data):
    return {
        'last': np.mean(stock_data.tail(1)),
        'short_mean': np.mean(stock_data.tail(20)),
        'long_mean': np.mean(stock_data.tail(200)),
        'short_rolling': stock_data.rolling(window=20).mean(),
        'long_rolling': stock_data.rolling(window=200).mean()
    }

#Plot those stats! Takes a column and who it belongs to, plots stats values
def make_plot(fed_col, ticker):
    stats = get_stats(fed_col)
    #plt.style.use('dark_background')
    plt.subplots(figsize=(6,4))
    plt.plot(fed_col, label=ticker)
    plt.plot(stats['short_rolling'], label='20 day rolling mean')
    plt.plot(stats['long_rolling'], label='200 day rolling mean')
    plt.xlabel("Date")
    #plt.ylabel("Adj Close (p)")
    plt.ylabel("Closing Price")
    plt.legend()
    plt.title("Stock Price Over Time.")
    
    plt.show()

#Takes ticker, gets data of stock, cleans adj_close,
#Makes a plot of adj close
def get_data(ticker):
    try:
        stock_data = data.DataReader(ticker, 'yahoo', START_DATE, END_DATE)
        #print(stock_data)
        adj_close = clean_data(stock_data, 'Close') #edited column
        make_plot(adj_close, ticker)

    except RemoteDataError:
        print("No Data found for {t}".format(t=ticker))

df = data.DataReader('AAPL', 'yahoo', START_DATE, END_DATE)
print(df.index) #this gives us the date index. now we can map dates vs dividends, price, etc
print( df.columns)

get_data(stock_1) #gives past closing dtaa, and the get_stats function can be edited to display what we want. can then do projections as we go on.
#could work on producing all graphs, or making this whole package call-able
