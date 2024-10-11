import plotly.graph_objects as go
import yfinance as yf
import pickle
import pandas as pd

# Step 1: Load financial data (including balance sheet and income statement) from pickle file
with open('../../allData.pkl', 'rb') as file:
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
    gross_profit = income_statement.loc['Gross Profit']
    cost_of_revenue = total_revenue - gross_profit
    operating_expense = income_statement.loc['Operating Expense']
    interest_expense = income_statement.loc['Interest Expense']
    total_expenses = operating_expense + cost_of_revenue + interest_expense
else:
    raise ValueError(f"Ticker {ticker} not found in the data.")

# Step 3: Get the current stock price using yfinance
stock_data = yf.Ticker(ticker)
share_price = stock_data.history(period='1d')['Close'][0]  # Get the latest closing price

# Step 4: Calculate Market Cap
market_cap = share_price * shares_outstanding

# Example periods for the slider (e.g., '2020', '2021', '2022', '2023')
periods = ['2020', '2021', '2022', '2023']  # Add more periods as per your dataset

# Dummy data for each period (replace with actual calculations for each year/period)
revenue_data = [total_revenue.values[0], total_revenue.values[0] * 1.05, total_revenue.values[0] * 1.1, total_revenue.values[0] * 1.15]
expense_data = [total_expenses.values[0], total_expenses.values[0] * 1.03, total_expenses.values[0] * 1.07, total_expenses.values[0] * 1.12]
market_cap_data = [market_cap, market_cap * 1.02, market_cap * 1.08, market_cap * 1.15]

# Step 5: Create the bar chart with a slider
fig = go.Figure()

# Add a single set of bars (these will update with the slider)
fig.add_trace(go.Bar(
    x=['Revenue', 'Expenses', 'Market Cap'],
    y=[revenue_data[0], expense_data[0], market_cap_data[0]],  # Initial values for the first period
    marker_color=['green', 'red', 'blue']
))

# Step 6: Create slider steps that update the y-values of the bars
steps = []
for i, period in enumerate(periods):
    step = dict(
        method="restyle",  # Update the bars' y-values
        args=[{"y": [[revenue_data[i], expense_data[i], market_cap_data[i]]]}],
        label=period
    )
    steps.append(step)

# Step 7: Add the slider to the layout
sliders = [dict(
    active=0,
    currentvalue={"prefix": "Period: "},
    pad={"t": 50},
    steps=steps
)]

# Step 8: Update layout
fig.update_layout(
    sliders=sliders,
    title=f"{ticker} Financial Data: Revenue, Expenses, Market Cap",
    yaxis_title="Value in $",
    xaxis_title="Categories",
    barmode='group'
)

# Step 9: Display the plot
fig.show()
