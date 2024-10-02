import yfinance as yf
import pickle

# Step 1: Load financial data (including balance sheet) from pickle file
with open('../allData.pkl', 'rb') as file:
    allData = pickle.load(file)

# Select the company ticker (e.g., 'KO')
ticker = 'KO'

# Step 2: Get financial data for the selected ticker
if ticker in allData:
    balance_sheet = allData[ticker]['balance_sheet']
    income_sheet = allData[ticker]['income_sheet']
    # Extract Shares Outstanding (typically in the Equity section, labeled as 'Common Stock' or similar)
    shares_outstanding = balance_sheet.loc['Ordinary Shares Number', 2022] # Adjust if labeled differently

    cost_of_revenue = income_sheet.loc['Cost of Revenue']
else:
    raise ValueError(f"Ticker {ticker} not found in the data.")


print(shares_outstanding)
print(cost_of_revenue)

# Step 3: Get the current stock price using yfinance
stock_data = yf.Ticker(ticker)
share_price = stock_data.history(period='1d')['Close'][0]  # Get the latest closing price

# Step 4: Calculate Market Cap
market_cap = share_price * shares_outstanding
print(f"Market Cap of {ticker}: ${market_cap:,}")
