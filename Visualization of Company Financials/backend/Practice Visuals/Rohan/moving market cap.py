import matplotlib.pyplot as plt
import matplotlib.animation as animation
import yfinance as yf
import pickle
import pandas as pd


# Function to get the average share price for a specific year
def get_average_share_price(ticker, year):
    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"
    stock_data = yf.Ticker(ticker)
    historical_data = stock_data.history(start=start_date, end=end_date)
    average_price = historical_data['Close'].mean()
    return average_price


# Load financial data and calculate market cap using average share price
def load_data(ticker, year):
    # Load financial data from pickle file
    with open('../../allData.pkl', 'rb') as file:
        allData = pickle.load(file)

    # Extract income statement and balance sheet for the company
    income_statement = allData[ticker]['income_statement']
    balance_sheet = allData[ticker]['balance_sheet']

    # Retrieve shares outstanding
    shares_outstanding = balance_sheet.loc['Ordinary Shares Number', year]
    if isinstance(shares_outstanding, pd.Series):
        shares_outstanding = shares_outstanding.iloc[0]

    # Get the average share price for the specific year
    average_share_price = get_average_share_price(ticker, year)

    # Calculate market cap
    market_cap = average_share_price * shares_outstanding

    return market_cap


# Define the company ticker
ticker = 'AAPL'  # Replace 'AAPL' with your desired ticker

# Retrieve market caps for specific years
years = ['2020', '2021', '2022', '2023']
market_caps = [load_data(ticker, year) for year in years]

# Animation setup
fig, ax = plt.subplots()
bar = ax.bar("Market Cap", market_caps[0], color='green')  # Initial market cap for the first year
ax.set_ylim(0, max(market_caps) * 1.2)  # Set y-limit for better visualization
ax.set_ylabel('Market Cap (in Billions)')
ax.set_title('Market Cap Over Time')


# Function to update the bar for each frame of animation
def update_bar(frame):
    year_idx = frame % len(market_caps)
    market_cap = market_caps[year_idx]
    bar[0].set_height(market_cap)
    ax.set_title(f'Market Cap for Year {years[year_idx]}')


# Create the animation
ani = animation.FuncAnimation(fig, update_bar, frames=100, repeat=True, interval=1000)  # Loop over 100 frames

# Show the animated plot
ax.axis('off')
plt.show()
