import plotly.graph_objects as go
import yfinance as yf
import pickle

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
    total_revenue = income_statement.loc['Total Revenue'].values[0]
    gross_profit = income_statement.loc['Gross Profit'].values[0]
    cost_of_revenue = total_revenue - gross_profit
    operating_expense = income_statement.loc['Operating Expense'].values[0]
    interest_expense = income_statement.loc['Interest Expense'].values[0]
    total_expenses = operating_expense + cost_of_revenue + interest_expense

    # Calculate final profit
    final_profit = total_revenue - total_expenses

else:
    raise ValueError(f"Ticker {ticker} not found in the data.")

# Step 3: Get the current stock price using yfinance
stock_data = yf.Ticker(ticker)
share_price = stock_data.history(period='1d')['Close'][0]  # Get the latest closing price

# Step 4: Calculate Market Cap
market_cap = share_price * shares_outstanding

# Step 5: Create the flow diagram
fig = go.Figure()

# Add the box where the income flows into and out of (representing all the data)
fig.add_shape(
    type="rect",
    x0=0.3, y0=0.3, x1=0.7, y1=0.7,
    line=dict(color="RoyalBlue"),
    fillcolor="LightSkyBlue",
    name="Data Box"
)

# Add an arrow representing the income flowing into the box (Total Revenue)
fig.add_annotation(
    x=0.25, y=0.5,
    ax=0, ay=0.5,
    xref="paper", yref="paper",
    axref="paper", ayref="paper",
    text=f"Total Revenue: ${total_revenue:,}",
    showarrow=True,
    arrowhead=3,
    arrowsize=2,
    arrowcolor="green",
    font=dict(size=12, color="green"),
)

# Add an arrow representing the final profit flowing out of the box
fig.add_annotation(
    x=0.75, y=0.5,
    ax=1, ay=0.5,
    xref="paper", yref="paper",
    axref="paper", ayref="paper",
    text=f"Final Profit: ${final_profit:,}",
    showarrow=True,
    arrowhead=3,
    arrowsize=2,
    arrowcolor="orange",
    font=dict(size=12, color="orange"),
)

# Add some additional details inside the box (like expenses, market cap)
fig.add_annotation(
    x=0.5, y=0.6,
    xref="paper", yref="paper",
    text=f"Expenses: ${total_expenses:,}",
    showarrow=False,
    font=dict(size=10),
)

fig.add_annotation(
    x=0.5, y=0.4,
    xref="paper", yref="paper",
    text=f"Market Cap: ${market_cap:,}",
    showarrow=False,
    font=dict(size=10),
)

# Set layout
fig.update_layout(
    title=f"{ticker} Income Flow Diagram",
    showlegend=False,
    xaxis=dict(visible=False),
    yaxis=dict(visible=False),
)

# Step 6: Display the flow diagram
fig.show()
