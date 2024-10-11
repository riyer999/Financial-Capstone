import plotly.express as px
import plotly.io as pio  # Import plotly.io for local display
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

    # Function to find the label containing a keyword
    def find_label(dataframe, keyword):
        for label in dataframe.index:
            if keyword.lower() in label.lower():
                return label
        raise KeyError(f"Label containing '{keyword}' not found in DataFrame index.")

    # Retrieve labels dynamically
    shares_label = find_label(balance_sheet, 'Ordinary Shares Number')
    liabilities_label = find_label(balance_sheet, 'Total Liabilities')
    assets_label = find_label(balance_sheet, 'Total Assets')
    income_label = find_label(income_statement, 'Net Income')
    revenue_label = find_label(income_statement, 'Total Revenue')

    # Retrieve scalar values safely (handling Series if returned)
    def get_scalar_value(df, label, year):
        value = df.loc[label, year]
        if isinstance(value, pd.Series):
            value = value.iloc[0]  # Take the first value if a Series is returned
        return value

    shares_outstanding = get_scalar_value(balance_sheet, shares_label, year)
    liabilities = get_scalar_value(balance_sheet, liabilities_label, year)
    assets = get_scalar_value(balance_sheet, assets_label, year)
    income = get_scalar_value(income_statement, income_label, year)
    revenue = get_scalar_value(income_statement, revenue_label, year)

    # Get the average share price for the specific year
    average_share_price = get_average_share_price(ticker, year)

    # Calculate market cap
    market_cap = average_share_price * shares_outstanding

    return {
        'year': year,
        'market_cap': market_cap,
        'income': income,
        'revenue': revenue,
        'assets': assets,
        'liabilities': liabilities
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

# Show the plot in the current environment (e.g., Jupyter notebook, etc.)
pio.show(fig)
