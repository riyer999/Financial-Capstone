import yfinance as yf #library allows to access financial data from Yahoo Finance
import pickle # used to save data to a file
#https://rfachrizal.medium.com/how-to-obtain-financial-statements-from-stocks-using-yfinance-87c432b803b8

#Import tickerList as a list
with open('0_tickerList.txt', 'r') as file: #contains ticker symbols, ticker means represents a stock of a certain company
    tickerList = [line.strip() for line in file.readlines()] #reads the ticker list

#Master dictionary is called allData
allData = {} #creating a dictionary to store the data for each ticker (apple and coca cola)
tickerList = ['AAPL','KO'] #overrides the tickerlist and only chooses to read these companies stocks
for ticker in tickerList: #for every ticker syymbol
    try:
        print(ticker)
        #Temp dictionary stores the info below
        temp = {}
        ystock = yf.Ticker(ticker)
        #temp['balance_sheet']=ystock.balance_sheet
        temp['income_statement']=ystock.incomestmt
        #temp['cashflow_statement']=ystock.cashflow
        #temp['info']=ystock.info
        #temp['hist']=ystock.history(period='5y')
        #Ticker, temp dict pair added to master dictionary
        allData[ticker] = temp
    except Exception as e:
        print('Error')

#Save data to allData.pkl file
with open('allData.pkl', 'wb') as file:
    pickle.dump(allData, file)






