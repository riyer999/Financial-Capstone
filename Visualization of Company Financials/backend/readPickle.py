import pickle
#this file isn't doing anything in the program right now.

# Load the data from the allData.pkl file
with open('allData.pkl', 'rb') as file:
    allData = pickle.load(file)

# Example: Accessing data for a specific ticker (e.g., 'AAPL')
ticker = 'KO'

# Access income statement
income_statement = allData[ticker]['income_statement']
#print("Income Statement:\n", income_statement)

# Access cash flow statement
cashflow_statement = allData[ticker]['cashflow_statement']
#print("Cash Flow Statement:\n", cashflow_statement)
gross_profit = income_statement.loc['Gross Profit']
print(gross_profit)


# Access company info
info = allData[ticker]['info']
#print("Company Info:\n", info)

 #Access balance sheet
balance_sheet = allData[ticker]['balance_sheet']
#print("Balance Sheet:\n", balance_sheet)

# Access historical data
history = allData[ticker]['hist']
#print("Historical Data (5 years):\n", history)
