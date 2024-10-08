import pickle

# Define the company ticker and year
ticker = 'AAPL'  # Replace 'KO' with the ticker you want
year = '2022'  # Replace with the specific year you want
# Step 1: Load financial data (including balance sheet) from pickle file
with open('../../allData.pkl', 'rb') as file:
    allData = pickle.load(file)
income_statement = allData[ticker]['income_statement']
balance_sheet = allData[ticker]['balance_sheet']
total_revenue = income_statement.loc['Cost Of Revenue', year]
ordinary_shares_number = balance_sheet.loc['Ordinary Shares Number', year]


print(ordinary_shares_number)
