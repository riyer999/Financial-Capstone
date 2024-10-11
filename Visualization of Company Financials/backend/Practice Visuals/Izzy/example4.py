import yfinance as yf
import pickle
import matplotlib.pyplot as plt

# Step 1: Load financial data (including balance sheet and income statement) from pickle file
with open('../../allData.pkl', 'rb') as file:
    allData = pickle.load(file)

# Select the company ticker (e.g., 'KO')
ticker = 'KO'

# Step 2: Get financial data for the selected ticker
if ticker in allData:
    balance_sheet = allData[ticker]['balance_sheet']
    income_statement = allData[ticker]['income_statement']

    # Extract Shares Outstanding
    shares_outstanding = balance_sheet.loc['Ordinary Shares Number', :].values[0]

    # Extract Total Revenue and Total Expenses
    total_revenue = income_statement.loc['Total Revenue']
    gross_profit = income_statement.loc['Gross Profit']
    cost_of_revenue = total_revenue - gross_profit
    operating_expense = income_statement.loc['Operating Expense']
    interest_expense = income_statement.loc['Interest Expense']
    total_expenses = operating_expense + cost_of_revenue + interest_expense

else:
    raise ValueError(f"Ticker {ticker} not found in the data.")

# Step 3: Get the current stock price using yfinance
stock_data = yf.Ticker(ticker)
share_price = stock_data.history(period='1d')['Close'].iloc[0]  # Get the latest closing price

# Step 4: Calculate Market Cap
market_cap = share_price * shares_outstanding

# Step 5: Extract the latest revenue and expenses
latest_revenue = total_revenue.values[0]  # The most recent revenue
latest_expense = total_expenses.values[0]  # The most recent expenses

# Total starting amount (incoming) and total final amount (outgoing)
total_starting_amount = latest_revenue
total_final_amount = total_starting_amount - latest_expense

# Step 6: Create the box with arrows
fig, ax = plt.subplots(figsize=(10, 6))

# Draw the box
box = plt.Rectangle((0.35, 0.4), 0.3, 0.4, edgecolor='black', facecolor='lightgray', linewidth=2)
ax.add_patch(box)

# Add incoming arrow (purple) pointing at the box's edge
ax.annotate('', xy=(0.4, 0.4), xytext=(0.25, 0.4),
            arrowprops=dict(arrowstyle='->', color='purple', lw=3, mutation_scale=15))

# Add outgoing arrow (green) pointing away from the box
ax.annotate('', xy=(0.7, 0.4), xytext=(0.85, 0.4),
            arrowprops=dict(arrowstyle='->', color='green', lw=3, mutation_scale=15))

# Add text for incoming amount above the arrow
ax.text(0.25, 0.43, f'Starting Amount: ${total_starting_amount:,.2f}', 
        fontsize=12, color='purple', verticalalignment='bottom', ha='right')

# Add information inside the box
ax.text(0.5, 0.75, 'Relevant Financial Information', 
        fontsize=14, ha='center', weight='bold')
ax.text(0.5, 0.65, f'Total Revenue: ${latest_revenue:,.2f}', 
        fontsize=12, ha='center')
ax.text(0.5, 0.60, f'Total Expenses: ${latest_expense:,.2f}', 
        fontsize=12, ha='center')
ax.text(0.5, 0.55, f'Market Cap: ${market_cap:,.2f}', 
        fontsize=12, ha='center')

# Add text for outgoing amount above the arrow
ax.text(0.85, 0.43, f'Final Amount: ${total_final_amount:,.2f}', 
        fontsize=12, color='green', verticalalignment='bottom', ha='left')

# Formatting the plot
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')  # Hide axes
ax.set_title(f'{ticker} Financial Overview', fontsize=16)

# Step 7: Save the figure and display it
plt.tight_layout()
plt.savefig(f'financial_overview_{ticker}.png')
plt.show()
