import yfinance as yf

# Create a Ticker object for Coca-Cola
ticker = 'KO'
ystock = yf.Ticker(ticker)

# Retrieve the income statement
income_statement = ystock.financials  # Updated method to fetch income statement

# Display the income statement
print(income_statement)
