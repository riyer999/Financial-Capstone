import matplotlib.pyplot as plt
import numpy as np
import pickle
import pandas as pd
import yfinance as yf

# Load financial data and define total_revenue
def load_data(ticker, year):
    with open('../allData.pkl', 'rb') as file:
        allData = pickle.load(file)
    income_statement = allData[ticker]['income_statement']
    balance_sheet = allData[ticker]['balance_sheet']

    # Get the total revenue for the specific year
    total_revenue = income_statement.loc['Total Revenue', year]
    cost_of_revenue = income_statement.loc['Cost Of Revenue', year]
    operating_expense = income_statement.loc['Operating Expense', year]
    interest_expense = income_statement.loc['Interest Expense', year]
    total_expenses = operating_expense + cost_of_revenue + interest_expense

    # Retrieve shares outstanding
    shares_outstanding = balance_sheet.loc['Ordinary Shares Number', year]
    if isinstance(shares_outstanding, pd.Series):
        shares_outstanding = shares_outstanding.iloc[0]

    # Fetch the share price using yfinance
    stock_data = yf.Ticker(ticker)
    share_price = stock_data.history(period='1d')['Close'].iloc[0]  # Get the latest closing price

    # Step 4: Calculate Market Cap
    market_cap = share_price * shares_outstanding  # Ensure both are numeric

    # Ensure total_revenue is a single scalar value, not a pandas Series
    if isinstance(total_revenue, pd.Series):
        total_revenue = total_revenue.iloc[0]

    if isinstance(total_expenses, pd.Series):
        total_expenses = total_expenses.iloc[0]

    return total_revenue, total_expenses, market_cap #function will return values for desired company

# Define the company ticker and year
ticker = 'KO'
year = '2022'

# Get total revenue, expenses, and market cap from data
total_revenue, total_expenses, market_cap = load_data(ticker, year)

# Example values
revenue = total_revenue
expenses = total_expenses

def draw_scale(revenue, expenses, market_cap):
    # Scale position variables
    base_width = 10
    base_height = 1
    beam_length = 12
    support_height = 6


    # Revenue and Expense scaling factor (to adjust size differences)
    max_weight = max(revenue, expenses)  # Ensure both revenue and expenses are single values
    revenue_scale = revenue / max_weight #scaling the values to ensure they fit properly in the visualization
    expense_scale = expenses / max_weight

    # sets the size of the overall plot
    fig, ax = plt.subplots(figsize=(20, 12))

    # Draw the base of the scale
    ax.plot([-base_width / 2, base_width / 2], [0, 0], color='brown', lw=4)

    # Draw the support
    ax.plot([0, 0], [0, support_height], color='black', lw=4)

    # Draw the beam of the scale
    ax.plot([-beam_length / 2, beam_length / 2], [support_height, support_height], color='gray', lw=4)

    # Draw the left plate (revenue side)
    left_plate_x = -beam_length / 2
    ax.plot([left_plate_x, left_plate_x], [support_height, support_height - 2 * revenue_scale], color='blue', lw=4)
    ax.text(left_plate_x, support_height - 2.5 * revenue_scale, f"Revenue: {revenue}", ha='center', color='blue')

    # Draw the right plate (expenses side)
    right_plate_x = beam_length / 2
    ax.plot([right_plate_x, right_plate_x], [support_height, support_height - 2 * expense_scale], color='red', lw=4)
    ax.text(right_plate_x, support_height - 2.5 * expense_scale, f"Expenses: {expenses}", ha='center', color='red')

    # Adjust the tilt of the scale based on revenue vs. expenses
    if revenue > expenses:
        tilt_angle = np.deg2rad(10)
    elif expenses > revenue:
        tilt_angle = np.deg2rad(-10)
    else:
        tilt_angle = 0

    # Apply the tilt (rotating the beam of the scale)
    for line in ax.lines[-3:]:
        x_data, y_data = line.get_data()
        x_tilted = x_data * np.cos(tilt_angle) - y_data * np.sin(tilt_angle)
        y_tilted = x_data * np.sin(tilt_angle) + y_data * np.cos(tilt_angle)
        line.set_data(x_tilted, y_tilted)

    # Set plot limits and title
    ax.set_xlim(-10, 10)
    ax.set_ylim(-3, 7)
    ax.set_title("Company Performance: Revenue vs. Expenses")

    # Hide axes
    ax.axis('off')

    # Add the market cap label at the top
    ax.text(0, support_height + 2, f"Market Cap: ${market_cap:,.0f}", ha='center', color='green', fontsize=12,
            fontweight='bold')

    # Show the plot
    plt.show()

# Call the draw_scale function with the actual revenue, expenses, and market cap
draw_scale(revenue, expenses, market_cap)
print(f"Total Revenue: ${total_revenue:,.2f}")
print(f"Total Expenses: ${total_expenses:,.2f}")
print(f"Market Cap: ${market_cap:,.2f}")
