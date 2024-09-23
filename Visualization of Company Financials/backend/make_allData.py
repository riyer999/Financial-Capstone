import yfinance as yf
import pickle
#https://rfachrizal.medium.com/how-to-obtain-financial-statements-from-stocks-using-yfinance-87c432b803b8

#Import tickerList as a list
with open('0_tickerList.txt', 'r') as file:
    tickerList = [line.strip() for line in file.readlines()]

#Master dictionary is called allData
allData = {}
tickerList = ['AAPL','KO', 'TSM', 'AMZN']
for ticker in tickerList:
    try:
        print(ticker)
        #Temp dictionary stores the info below
        temp = {}
        ystock = yf.Ticker(ticker)
        temp['balance_sheet']=ystock.balance_sheet
        temp['income_statement']=ystock.incomestmt
        temp['cashflow_statement']=ystock.cashflow
        temp['info']=ystock.info
        temp['hist']=ystock.history(period='5y')
        #Ticker, temp dict pair added to master dictionary
        allData[ticker] = temp
    except Exception as e:
        print('Error')

#Save data to allData.pkl file
with open('allData.pkl', 'wb') as file:
    pickle.dump(allData, file)


#THIS FILE GENERATES THE allData.pkl





