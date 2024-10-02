import yfinance as yf
import pickle
import matplotlib.pyplot as plt

# Step 1: Load financial data (including balance sheet and income statement) from pickle file
with open('../allData.pkl', 'rb') as file:
    allData = pickle.load(file)

# Select the company ticker (e.g., 'KO')
ticker = 'KO'

# Step 2: Get financial data for the selected ticker
if ticker in allData:
    balance_sheet = allData[ticker]['balance_sheet']
    income_statement = allData[ticker]['income_statement']

    # Extract Shares Outstanding (typically in the Equity section, labeled as 'Ordinary Shares Number')
    shares_outstanding = balance_sheet.loc['Ordinary Shares Number', :].values[0]  # Adjust if labeled differently

    # Extract Total Revenue and Total Expenses (e.g., Operating Expense)
    total_revenue = income_statement.loc['Total Revenue']
    #left side of the scale
    gross_profit = income_statement.loc['Gross Profit']
    print(gross_profit)
    cost_of_revenue = total_revenue - gross_profit
    operating_expense = income_statement.loc['Operating Expense']
    interest_expense = income_statement.loc['Interest Expense']
    total_expenses = operating_expense + cost_of_revenue + interest_expense

else:
    raise ValueError(f"Ticker {ticker} not found in the data.")

print(total_revenue)
print("total expenses", total_expenses)




# Step 3: Get the current stock price using yfinance
stock_data = yf.Ticker(ticker)
share_price = stock_data.history(period='1d')['Close'][0]  # Get the latest closing price

# Step 4: Calculate Market Cap
market_cap = share_price * shares_outstanding
print(f"Market Cap of {ticker}: ${market_cap:,}")

# Step 5: Extract the latest revenue and expenses
latest_revenue = total_revenue.values[0]  # The most recent revenue
latest_expense = total_expenses.values[0]  # The most recent expenses

# Step 6: Create a combined visualization
fig, ax = plt.subplots(figsize=(10, 6))

# Set the scale based on the highest value (revenue, expenses, or market cap)
max_value = max(latest_revenue, latest_expense, market_cap) * 1.2

# Draw the balance scale base line
ax.plot([0, 1], [0, 0], color='black', lw=4)

# Plot revenue, expenses, and market cap as bars
ax.barh(0.2, latest_revenue, height=0.2, color='green', label=f'Revenue: ${latest_revenue:,}')
ax.barh(0, latest_expense, height=0.2, color='red', label=f'Expenses: ${latest_expense:,}')
ax.barh(-0.2, market_cap, height=0.2, color='blue', label=f'Market Cap: ${market_cap:,}')

# Add balance point (for simplicity, centered)
balance_point = (latest_revenue - latest_expense) / max_value
ax.plot([0.5 + balance_point / 2, 0.5 - balance_point / 2], [0.2, 0], color='black', lw=2)

# Formatting and labels
ax.set_xlim(0, max_value)
ax.set_ylim(-0.5, 0.5)
ax.set_xticks([])
ax.set_yticks([])
ax.set_title(f'{ticker} Balance Scale: Revenue vs Expenses vs Market Cap', fontsize=14)
ax.legend()

# Step 7: Save the figure and display it
plt.tight_layout()
plt.savefig(f'balance_scale_{ticker}.png')
plt.show()
