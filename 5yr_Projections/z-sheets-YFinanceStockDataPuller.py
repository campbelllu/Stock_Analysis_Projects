#documentation for yf: https://pypi.org/project/yfinance/ 
#documentation for financial ratios to calculate: https://www.investopedia.com/financial-edge/0910/6-basic-financial-ratios-and-what-they-tell-you.aspx

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


stock_1 = yf.Ticker("AAPL") #apple for easy test

#print(stock_1.history(period="max"))#info['trailingAnnualDividendRate'])

df = pd.DataFrame(stock_1.history(period="max")) #we get financial data
df.to_csv('testFrame.csv')
##df2 = pd.DataFrame() #blank df
##for i in range(df.index.len()-1): #look over whole data frame
##    if df.index['i'] > '2016-01-01': #populate the date column
##        df2.append(['Date'])

        
print(df.head())
print(df.columns)
print(df.index)
##plt.subplots(figsize=(6,4))
##plt.plot(stock_1.info, label="AAPL")
##plt.xlabel("Date")
##plt.ylabel("Close")
##plt.legend()
##plt.title("stock price over time")




#prices over time
#dividends over time from yahoo finance site
###aapl, predict where it's going for both
#p/e, (ticker.info['trailingPE']) #trailing gives evidence, forward is estimate on performance. don't use it

#trailingAnnualDividendRate: avg from TTM, allows for regression if access to twelve points is known
#dividendRate: how much a company pays out in dividends each year relative to its stock price; might be okay to ignore; current

###dividendYield: most recent full year dividend over current share price, (annual div)/(current stock price)
#fiveYearAvgDividendYield: Like above but over time
#trailingAnnualDividendYield: TTM of divYield

#
