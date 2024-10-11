import plotly.express as px # type: ignore
import yfinance as yf # type: ignore
import pickle
import pandas as pd # type: ignore

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

    return {
        'year': year,
        'market_cap': market_cap,
        'income': income_statement.loc['Net Income', year],
        'revenue': income_statement.loc['Total Revenue', year],
        'assets': balance_sheet.loc['Total Assets', year],
        'liabilities': balance_sheet.loc['Total Liabilities', year]
    }

# Define the company ticker
ticker = 'AAPL'  # Replace 'AAPL' with your desired ticker

# Retrieve financial data for specific years
years = ['2020', '2021', '2022', '2023']
financial_data = [load_data(ticker, year) for year in years]

# Create a dataframe from the financial data
df = pd.DataFrame(financial_data)

# Create a sunburst plot
fig = px.sunburst(
    df,
    path=['year', 'income', 'revenue', 'assets', 'liabilities'],
    values='market_cap',  # The value used to determine the size of the segments
    color='market_cap',  # The value used to color the segments
    color_continuous_scale='Viridis',
    title="Sunburst of Financial Data by Year"
)

# Show the plot
fig.show()
