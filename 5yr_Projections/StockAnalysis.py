#stock earnings comparison
#assumings zero crashes, under the idea that each crash would equally affect each ETF
#assumes monthly compounding and dividend payments for all
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math

#stock info, manually gathered-------------------------------------------------------------------------------------------------
#############S&P's: VOO
VOO = {'Name': 'VOO', 'Price': 400, 'Growth': 0.0142, 'Bad_Growth': 0.138, 'Div_Yield': 0.0134, 'Expenses': 0.0003,
       'Div_Returned': 0, 'Shares_Owned': 0, 'Equity': 0, 'Total_Expenses': 0, 'Funds_Invested': 0, 'Fees_Paid': 0
      }

############Growth's:
SCHG = {'Name': 'SCHG', 'Price': 150, 'Growth': 0.0242, 'Bad_Growth': 0.23, 'Div_Yield': 0.0043, 'Expenses': 0.0004,
        'Div_Returned': 0, 'Shares_Owned': 0, 'Equity': 0, 'Total_Expenses': 0, 'Funds_Invested': 0, 'Fees_Paid': 0
      }

RPG = {'Name': 'RPG', 'Price': 190, 'Growth': 0.0212, 'Bad_Growth': 0.20, 'Div_Yield': 0.0017, 'Expenses': 0.0035,
       'Div_Returned': 0, 'Shares_Owned': 0, 'Equity': 0, 'Total_Expenses': 0, 'Funds_Invested': 0, 'Fees_Paid': 0
      }

VUG = {'Name': 'VUG', 'Price': 290, 'Growth': 0.02374, 'Bad_Growth': 0.228, 'Div_Yield': 0.0057, 'Expenses': 0.0004,
       'Div_Returned': 0, 'Shares_Owned': 0, 'Equity': 0, 'Total_Expenses': 0, 'Funds_Invested': 0, 'Fees_Paid': 0
      }

QQQ = {'Name': 'QQQ', 'Price': 365, 'Growth': 0.025999, 'Bad_Growth': 0.249, 'Div_Yield': 0.0049, 'Expenses': 0.002,
       'Div_Returned': 0, 'Shares_Owned': 0, 'Equity': 0, 'Total_Expenses': 0, 'Funds_Invested': 0, 'Fees_Paid': 0
      }

ARKK = {'Name': 'ARKK', 'Price': 100, 'Growth': 0.049999, 'Bad_Growth': 0.4797, 'Div_Yield': 0.00, 'Expenses': 0.0075,
        'Div_Returned': 0, 'Shares_Owned': 0, 'Equity': 0, 'Total_Expenses': 0, 'Funds_Invested': 0, 'Fees_Paid': 0
      }

############Div's:
VIG = {'Name': 'VIG', 'Price': 160, 'Growth': 0.0179, 'Bad_Growth': 0.173, 'Div_Yield': 0.0156, 'Expenses': 0.006,
       'Div_Returned': 0, 'Shares_Owned': 0, 'Equity': 0, 'Total_Expenses': 0, 'Funds_Invested': 0, 'Fees_Paid': 0
      }

VYM = {'Name': 'VYM', 'Price': 110, 'Growth': 0.0169, 'Bad_Growth': 0.162, 'Div_Yield': 0.0279, 'Expenses': 0.006,
       'Div_Returned': 0, 'Shares_Owned': 0, 'Equity': 0, 'Total_Expenses': 0, 'Funds_Invested': 0, 'Fees_Paid': 0
      }

QYLD = {'Name': 'QYLD', 'Price': 23, 'Growth': 0.011333, 'Bad_Growth': 0.108, 'Div_Yield': 0.118, 'Expenses': 0.006,
        'Div_Returned': 0, 'Shares_Owned': 0, 'Equity': 0, 'Total_Expenses': 0, 'Funds_Invested': 0, 'Fees_Paid': 0
      }

#methods for stock manipulation---------------------------------------------------------------------------------------------------------
def grow_stock(dikt): #moves stock value forward one month, changes stock price
    dikt['Price'] = dikt['Price']*(1+(dikt['Growth']))

def buy_stock(dikt, funds): #allows for partial share ownership, changes shares owned
    dikt['Shares_Owned'] += funds / dikt['Price']
    dikt['Equity'] = (dikt['Shares_Owned'] * dikt['Price']) #"$"+"{:,.2f}".format((dikt['Shares_Owned'] * dikt['Price']))
   # dikt['Funds_Invested'] += funds 

def divs_calculated(dikt):
    dikt['Div_Returned'] = dikt['Shares_Owned']*dikt['Price']*dikt['Div_Yield']
    return dikt['Div_Returned']

def divs_pay_fees(dikt, funds):
    divs = divs_calculated(dikt) #calculate monthly dividends
    fee_funds = divs + funds #calculate divs + funds
    remainder_fund =  fee_funds - dikt['Total_Expenses'] #pay fees with dividends + funds and return remainder for later use
    return remainder_fund

def expenses_due(dikt): #updates fees for stock ownership
    dikt['Total_Expenses'] = dikt['Shares_Owned']*dikt['Price']*dikt['Expenses']

#list for updating following methods, keeping it DRY, followed by methods-----------------------------------------------------------------
list_columns = ['Name', 'Price', 'Shares_Owned', 'Div_Returned', 'Total_Expenses', 'Equity', 'Funds Invested', 'Fees Paid']
#what do we want to see in our df?
#name, price, shares owned, divs returned each iteration, expenses paid each year, equity, funds invested,  total fees paid
def useable_list(dikt):
    return [dikt['Name'], dikt['Price'], dikt['Shares_Owned'], dikt['Div_Returned'], dikt['Total_Expenses'],
              dikt['Equity'], dikt['Funds_Invested'], dikt['Fees_Paid']]

def make_list(dikt):
    stock_list = []
    stock_list.append(useable_list(dikt))
    return stock_list

def update_list(dikt, slist):
    stock_list = slist #get list, then add to it
    stock_list.append(useable_list(dikt))
    return stock_list #give back updated list

def make_df(list1): #turn a list into a df
    df = pd.DataFrame(list1, columns=list_columns)
    return df

#investment methods------------------------------------------------------------------------------------------------------------------------
#go through t months, adjust ownership and stock price, log each step into df
def invest_monthly_returns(dikt, t, funds): #returns data frame for stock projections
    tracker = 0
    ref_list = make_list(dikt)

    while tracker <= t:
        if tracker == 0: #1. if tracker ==0, buy initial stock, never triggers again
            buy_stock(dikt, funds)
            dikt['Funds_Invested'] += funds
            #print("first buy")
        elif (tracker+1) % 12 == 0: #2. year end, pay fees before buying stock
            expenses_due(dikt) #determines fees due
            if dikt['Total_Expenses'] >= funds: #use dividends + funds to pay for fees
                remainder = divs_pay_fees(dikt, funds)
                buy_stock(dikt, remainder) #plug remainder into buy stocks function
                dikt['Funds_Invested'] += funds
                dikt['Fees_Paid'] += dikt['Total_Expenses']
              #  print("paid at year end with divs")
            else:
                remainder = funds - dikt['Total_Expenses'] #use funds to pay for fees
                divs = divs_calculated(dikt)#use divs and remainder to buy stocks function
                new_fund = remainder + divs
                buy_stock(dikt, new_fund)
                dikt['Funds_Invested'] += funds
                dikt['Fees_Paid'] += dikt['Total_Expenses']
                #print("paid at year end with funds")
        else: #3. not initial purchase, no fees due, get divs and buy stock
            divs = divs_calculated(dikt)
            new_fund = funds + divs
            buy_stock(dikt, new_fund)
            dikt['Funds_Invested'] += funds
           # print("no fees, bought stock")
            
        #6. update expenses, grow stock, increase tracker, update list               
        grow_stock(dikt) #update price for next interation        
        tracker += 1 #next data point ready to generate
        ref_list = update_list(dikt, ref_list)
        dikt['Total_Expenses'] = 0 #return fees due to 0 for df accuracy

    df = make_df(ref_list)
    return df

#inputs and csv creation-----------------------------------------------------------------------------------------------------------
fundings = 1000
time_in = 60

def df_to_csv(name, df): #input name in quotes.txt
    df.to_csv(name,index="False")
    print("CSV created for \n{}".format(df.head()))

#print df to test iterator---------------------------------------------------------------------------------------------------------
#pd.set_option("display.max_columns", None)
#print(invest_monthly_returns(QYLD, time_in, fundings))



#create all the csv's of data
##df_to_csv("SCHG.csv", invest(SCHG, time_in, fundings))
##df_to_csv("RPG.csv", invest(RPG, time_in, fundings))
##df_to_csv("VUG.csv", invest(VUG, time_in, fundings))
##df_to_csv("QQQ.csv", invest(QQQ, time_in, fundings))
##df_to_csv("ARKK.csv", invest(ARKK, time_in, fundings))
df_to_csv("VOO.csv", invest_monthly_returns(VOO, time_in, fundings))
##df_to_csv("VIG.csv", invest(VIG, time_in, fundings))
##df_to_csv("VYM.csv", invest(VYM, time_in, fundings))
    #completed
##df_to_csv("QYLD.csv", invest_monthly_returns(QYLD, time_in, fundings))

#------------------------------------------------------------------------------------------------------------------------------------
#graph data from those csv's above

#take data from csv, make a df for use, plot from df


