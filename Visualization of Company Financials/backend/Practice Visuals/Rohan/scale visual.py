import matplotlib.pyplot as plt
import numpy as np
import pickle
import pandas as pd
import yfinance as yf  # need all these libraries to run the program


def get_average_share_price(ticker, year):
    # Define the start and end date for the year
    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"

    # Download historical data for the specific year
    stock_data = yf.Ticker(ticker)
    historical_data = stock_data.history(start=start_date, end=end_date)

    # Calculate the average closing price
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

    # Get the total revenue for the specific year
    total_revenue = income_statement.loc['Total Revenue', year].item()  # Convert to scalar

    # Retrieve individual expenses
    gross_profit = income_statement.loc['Gross Profit', year].item()  # Convert to scalar
    cost_of_revenue = total_revenue - gross_profit
    operating_expense = income_statement.loc['Operating Expense', year].item()  # Convert to scalar
    interest_expense = income_statement.loc['Interest Expense', year].item()  # Convert to scalar
    total_expenses = cost_of_revenue + operating_expense + interest_expense

    # Retrieve shares outstanding
    shares_outstanding = balance_sheet.loc['Ordinary Shares Number', year]
    if isinstance(shares_outstanding, pd.Series):
        shares_outstanding = shares_outstanding.iloc[0]  # In case it's a series, take the first value

    # Get the average share price for the specific year
    average_share_price = get_average_share_price(ticker, year)

    # Calculate Market Cap using the average share price for the year
    market_cap = average_share_price * shares_outstanding  # Ensure both are numeric

    return total_revenue, cost_of_revenue, operating_expense, interest_expense, market_cap


# Define the company ticker and year
ticker = 'AAPL'  # Replace 'AAPL' with the ticker you want
year = '2022'  # Replace with the specific year you want

# Return the financial data
total_revenue, cost_of_revenue, operating_expense, interest_expense, market_cap = load_data(ticker, year)


def draw_scale(revenue, cost_of_revenue, operating_expense, interest_expense, market_cap): #responsible for drawing a visual scale and comparing revenue and expenses
    # Scale position variables
    base_width = 6 # sets the width of the red base
    base_height = 1
    beam_length = 12
    support_height = 3

    # Total expenses
    total_expenses = cost_of_revenue + operating_expense + interest_expense

    # Scaling factors for expenses
    max_expense = max(total_expenses, revenue)  # Ensure both total_expenses and revenue are single values
    revenue_scale = revenue / max_expense #scaling all the values relative to each other
    total_expense_scale = total_expenses / max_expense #get that by dividing each by the max value
    cost_of_revenue_scale = cost_of_revenue / max_expense
    operating_expense_scale = operating_expense / max_expense
    interest_expense_scale = interest_expense / max_expense
    # Scaling factor for market cap relative to revenue and total expenses
    market_cap_scale = market_cap / max_expense  # Scale the market cap relative to the max of revenue or expenses

    # Set the size of the overall plot
    fig, ax = plt.subplots(figsize=(25, 15)) #size of the screen 25 * 15 units

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

    # Draw the blocks for total expenses on the right side
    right_plate_x = beam_length / 2
    ax.plot([right_plate_x, right_plate_x], [support_height, support_height - 2 * total_expense_scale], color='red', lw=4)
    ax.text(right_plate_x, support_height - 2.5 * total_expense_scale, f"Total Expenses: {total_expenses}", ha='center',
            color='red')


    # Draw individual expense blocks stacked on the right side
    # Set new x position for the stacked blocks
    stack_x_position = right_plate_x + -1.5  # Adjust this for left/right positioning

    # Cumulative height for the stacked expenses
    current_height = support_height + 2.5  # Start at the support height

    # Cost of Revenue Block
    current_height -= 2 * cost_of_revenue_scale  # Move down for the cost of revenue
    ax.add_patch(plt.Rectangle((stack_x_position, current_height), 1, 2 * cost_of_revenue_scale, color='orange'))
    ax.text(stack_x_position + 0.5, current_height + cost_of_revenue_scale, f"Cost of Revenue: {cost_of_revenue}",
            ha='center', color='black')

    # Operating Expense Block
    current_height -= 2 * operating_expense_scale  # Move down for the operating expense
    ax.add_patch(plt.Rectangle((stack_x_position, current_height), 1, 2 * operating_expense_scale, color='purple'))
    ax.text(stack_x_position + 0.5, current_height + operating_expense_scale, f"Operating Expense: {operating_expense}",
            ha='center', color='black')

    # Interest Expense Block
    current_height -= 2 * interest_expense_scale  # Move down for the interest expense
    ax.add_patch(plt.Rectangle((stack_x_position, current_height), 1, 2 * interest_expense_scale, color='green'))
    ax.text(stack_x_position + 0.5, current_height + interest_expense_scale, f"Interest Expense: {interest_expense}",
            ha='center', color='black')
    # Draw the Total Revenue as a stacked block on the left side
    total_revenue_x_position = left_plate_x - 1.0  # Positioning the Total Revenue block
    current_revenue_height = support_height + 1  # Start at the support height for stacking

    # Total Revenue Block
    current_revenue_height -= 2 * revenue_scale  # Move down for the total revenue
    ax.add_patch(plt.Rectangle((total_revenue_x_position, current_revenue_height), 1, 2 * revenue_scale, color='blue'))
    ax.text(total_revenue_x_position + 0.5, current_revenue_height + revenue_scale, f"Total Revenue: {revenue}",
            ha='center', color='black')

    # Adjust x and y positions
    market_cap_x_position = beam_length / 2 + 3  # Adjust this value to move the bar left or right (x-axis)
    market_cap_y_position = support_height - 9  # Adjust this value to move the bar up or down (y-axis)

    # Add the market cap bar
    ax.add_patch(plt.Rectangle((market_cap_x_position, market_cap_y_position), 1, 2 * market_cap_scale, color='green'))

    # Add label for the market cap
    ax.text(market_cap_x_position + 0.5, market_cap_y_position + market_cap_scale,
            f"Market Cap: ${market_cap:,.0f}", ha='center', color='black', fontsize=10)

    # Adjust the tilt of the scale based on revenue vs. total expenses, proportionally
    max_tilt_angle_deg = 20  # Maximum possible tilt in degrees
    difference = revenue - total_expenses  # Positive if revenue > expenses, negative otherwise
    max_value = max(revenue, total_expenses)  # Normalize by the larger value

    # Proportional tilt: the larger the difference, the more tilt, capped at max_tilt_angle_deg
    tilt_angle_deg = (difference / max_value) * max_tilt_angle_deg
    tilt_angle = np.deg2rad(tilt_angle_deg)  # Convert to radians for the tilt

    # Apply the tilt (rotating the beam of the scale)
    for line in ax.lines[-3:]:
        x_data, y_data = line.get_data()
        x_tilted = x_data * np.cos(tilt_angle) - y_data * np.sin(tilt_angle)
        y_tilted = x_data * np.sin(tilt_angle) + y_data * np.cos(tilt_angle)
        line.set_data(x_tilted, y_tilted)

    # Set plot limits
    ax.set_xlim(-10, 10)
    ax.set_ylim(-5, 7)

    # Add the title at the bottom
    ax.text(0, -3, "Company Performance: Revenue vs. Expenses", ha='center', fontsize=16, fontweight='bold')

    # Hide axes
    ax.axis('off')

    # Add the market cap label at the top
    ax.text(0, support_height + 2, f"Market Cap: ${market_cap:,.0f}", ha='center', color='green', fontsize=12,
            fontweight='bold')

    # Show the plot
    plt.show()


# Call the draw_scale function with the actual revenue, individual expenses, and market cap
draw_scale(total_revenue, cost_of_revenue, operating_expense, interest_expense, market_cap)

# Print financial metrics
print(f"Total Revenue: ${total_revenue:,.2f}")
print(f"Cost of Revenue: ${cost_of_revenue:,.2f}")
print(f"Operating Expenses: ${operating_expense:,.2f}")
print(f"Interest Expenses: ${interest_expense:,.2f}")
print(f"Total Expenses: ${cost_of_revenue + operating_expense + interest_expense:,.2f}")
print(f"Market Cap: ${market_cap:,.2f}")
x = get_average_share_price("AAPL", 2022)
print(f"Average Share Price: ${x:,.2f}")

