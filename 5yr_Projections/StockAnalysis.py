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
       'Div_Returned': 0, 'Shares_Owned': 0, 'Equity': 0
      }

############Growth's:
SCHG = {'Name': 'SCHG', 'Price': 150, 'Growth': 0.0242, 'Bad_Growth': 0.23, 'Div_Yield': 0.0043, 'Expenses': 0.0004,
        'Div_Returned': 0, 'Shares_Owned': 0, 'Equity': 0
      }

RPG = {'Name': 'RPG', 'Price': 190, 'Growth': 0.0212, 'Bad_Growth': 0.20, 'Div_Yield': 0.0017, 'Expenses': 0.0035,
       'Div_Returned': 0, 'Shares_Owned': 0, 'Equity': 0
      }

VUG = {'Name': 'VUG', 'Price': 290, 'Growth': 0.02374, 'Bad_Growth': 0.228, 'Div_Yield': 0.0057, 'Expenses': 0.0004,
       'Div_Returned': 0, 'Shares_Owned': 0, 'Equity': 0
      }

QQQ = {'Name': 'QQQ', 'Price': 365, 'Growth': 0.025999, 'Bad_Growth': 0.249, 'Div_Yield': 0.0049, 'Expenses': 0.002,
       'Div_Returned': 0, 'Shares_Owned': 0, 'Equity': 0
      }

ARKK = {'Name': 'ARKK', 'Price': 100, 'Growth': 0.049999, 'Bad_Growth': 0.4797, 'Div_Yield': 0.00, 'Expenses': 0.0075,
        'Div_Returned': 0, 'Shares_Owned': 0, 'Equity': 0
      }

############Div's:
VIG = {'Name': 'VIG', 'Price': 160, 'Growth': 0.0179, 'Bad_Growth': 0.173, 'Div_Yield': 0.0156, 'Expenses': 0.006,
       'Div_Returned': 0, 'Shares_Owned': 0, 'Equity': 0
      }

VYM = {'Name': 'VYM', 'Price': 110, 'Growth': 0.0169, 'Bad_Growth': 0.162, 'Div_Yield': 0.0279, 'Expenses': 0.006,
       'Div_Returned': 0, 'Shares_Owned': 0, 'Equity': 0
      }

QYLD = {'Name': 'QYLD', 'Price': 23, 'Growth': 0.011333, 'Bad_Growth': 0.108, 'Div_Yield': 0.118, 'Expenses': 0.006,
        'Div_Returned': 0, 'Shares_Owned': 0, 'Equity': 0, 'Total_Expenses': 0
      }



#methods for stock manipulation
def grow_stock(dikt): #moves stock value forward one month, changes stock price
    dikt['Price'] = dikt['Price']*(1+(dikt['Growth']))

def buy_stock(dikt, funds): #allows for partial share ownership, changes shares owned
    dikt['Shares_Owned'] += funds / dikt['Price']
    dikt['Equity'] = (dikt['Shares_Owned'] * dikt['Price']) #"$"+"{:,.2f}".format((dikt['Shares_Owned'] * dikt['Price']))

def divs_calculated(dikt):
    dikt['Div_Returned'] = dikt['Shares_Owned']*dikt['Price']*dikt['Div_Yield']
    
def divs_buy_stock(dikt): #calcs divs at beg of month, buys partial shares with divs ----------------------------------------------------------------HERE 1
    dikt['Div_Returned'] = dikt['Shares_Owned']*dikt['Price']*dikt['Div_Yield']
    if dikt['Div_Returned'] > 0:
        dikt['Shares_Owned'] += dikt['Div_Returned'] / dikt['Price']

#we also want to be able to pay our fees with dividend returns, eventually, to expand our timeframe of investments
def divs_pay_fees(dikt):#---------------------------------------------------------------------------------------------------------------------------HERE for fee payment
    
    break #placeholder while building function

def expenses_paid(dikt): #updates fees for stock ownership
    dikt['Total_Expenses'] = dikt['Shares_Owned']*dikt['Price']*dikt['Expenses']

#list for updating following methods, keeping it DRY
list_columns = ['Name', 'Price', 'Shares_Owned', 'Div_Returned', 'Total_Expenses', 'Equity']
#what do we want to see in our df?
#name, price, shares owned, divs returned each iteration, expenses paid each year, equity
def useable_list(dikt):
    return [dikt['Name'], dikt['Price'], dikt['Shares_Owned'], dikt['Div_Returned'], dikt['Total_Expenses'], dikt['Equity']]

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

#go through t months, adjust ownership and stock price, log each step into df
def invest(dikt, t, funds): #returns data frame for stock projections
    tracker = 0
    ref_list = make_list(dikt)

    while tracker <= t:
        #divs_buy_stock(dikt) #1. divs buy stock ----------------------------------------------------------------HERE 1

        if tracker == 0: #2. if tracker ==0, buy initial stock, never triggers again
            buy_stock(dikt, funds)
        #need to make this next elif never trigger by paying fees with dividend funds over time    ----------------------------------------------------------------HERE to cut out
        elif dikt['Total_Expenses'] >= funds: #3. check expenses, if exceed investment funds, stop investing
            print("Investing funds only pay fees.")
            break #breaks loop when fees exceed what's invested each month
        elif (tracker+1) % 12 == 0: #4. year end, pay fees before buying stock
            if dikt['Total_Expenses'] >= funds:
                #use dividends + funds to pay for fees, return ----------------------------------------------------------------HERE to pay fees indefinitely and never cut out
            buy_stock(dikt, (funds-dikt['Total_Expenses']))
        else:
            buy_stock(dikt, funds) #5. else: buy stock
        
        #6. update expenses, grow stock, increase tracker, update list               
        expenses_paid(dikt)
        #print(dikt['Total_Expenses'])
        grow_stock(dikt) #update price for next interation        
        tracker += 1 #next data point ready to generate
        ref_list = update_list(dikt, ref_list)

    df = make_df(ref_list)
    return df

def df_to_csv(name, df): #input name in quotes.txt
    df.to_csv(name,index="False")
    print("CSV created for \n{}".format(df.head()))


#inputs and csv creation-----------------------------------------------------------------------------------------------------
fundings = 1000
time_in = 5

#print df to test iterator---------------------------------------------------------------------------------------------------------
print(invest(QYLD, time_in, fundings))



#create all the csv's of data
##df_to_csv("SCHG.csv", invest(SCHG, time_in, fundings))
##df_to_csv("RPG.csv", invest(RPG, time_in, fundings))
##df_to_csv("VUG.csv", invest(VUG, time_in, fundings))
##df_to_csv("QQQ.csv", invest(QQQ, time_in, fundings))
##df_to_csv("ARKK.csv", invest(ARKK, time_in, fundings))
##df_to_csv("VOO.csv", invest(VOO, time_in, fundings))
##df_to_csv("VIG.csv", invest(VIG, time_in, fundings))
##df_to_csv("VYM.csv", invest(VYM, time_in, fundings))
##df_to_csv("QYLD.csv", invest(QYLD, time_in, fundings))

#------------------------------------------------------------------------------------------------------------------------------------
#graph data from those csv's above

#take data from csv, make a df for use, plot from df


