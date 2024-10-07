import pickle

# Define the company ticker and year
ticker = 'KO'  # Replace 'KO' with the ticker you want
year = '2022'  # Replace with the specific year you want
# Step 1: Load financial data (including balance sheet) from pickle file
with open('../../allData.pkl', 'rb') as file:
    allData = pickle.load(file)
income_statement = allData[ticker]['income_statement']

total_revenue = income_statement.loc['Cost Of Revenue', year]
print(total_revenue)
print(income_statement)
