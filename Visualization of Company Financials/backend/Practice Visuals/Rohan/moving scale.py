import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pickle
import pandas as pd
import yfinance as yf  # need all these libraries to run the code
from matplotlib.animation import FFMpegWriter



def get_average_share_price(ticker, year): #used to calculate the market cap over the past 3 years
    start_date = f"{year}-01-01" #to get the average you get all the shares
    end_date = f"{year}-12-31" #end date and start date to get the average closing price
    stock_data = yf.Ticker(ticker) #represents which company we are trying to get
    historical_data = stock_data.history(start=start_date, end=end_date) #computing the average closign price for that year
    average_price = historical_data['Close'].mean()
    return average_price


def load_data(ticker, year): #loads the financial data.
    with open('../../allData.pkl', 'rb') as file: #dictionary with the financial data informtion
        allData = pickle.load(file)

    income_statement = allData[ticker]['income_statement']
    balance_sheet = allData[ticker]['balance_sheet']

    total_revenue = income_statement.loc['Total Revenue', year].item()
    gross_profit = income_statement.loc['Gross Profit', year].item()
    cost_of_revenue = total_revenue - gross_profit
    operating_expense = income_statement.loc['Operating Expense', year].item()
    interest_expense = income_statement.loc['Interest Expense', year].item()
    total_expenses = cost_of_revenue + operating_expense + interest_expense

    shares_outstanding = balance_sheet.loc['Ordinary Shares Number', year] #getting the ordinary shares number for the year
    if isinstance(shares_outstanding, pd.Series): #select the first value in the pandas series
        shares_outstanding = shares_outstanding.iloc[0] #this is to get the most recent

    average_share_price = get_average_share_price(ticker, year)
    market_cap = average_share_price * shares_outstanding
    return total_revenue, cost_of_revenue, operating_expense, interest_expense, market_cap


def draw_scale(ax, revenue, cost_of_revenue, operating_expense, interest_expense, market_cap): #drawing a scale taking in these parameters
    base_width = 6
    base_height = 1
    beam_length = 12
    support_height = 3

    total_expenses = cost_of_revenue + operating_expense + interest_expense #what I am considering in the total expenses, not including some stuff like taxes
    max_expense = max(total_expenses, revenue) #scaling everything to the max value
    revenue_scale = revenue / max_expense
    total_expense_scale = total_expenses / max_expense
    cost_of_revenue_scale = cost_of_revenue / max_expense
    operating_expense_scale = operating_expense / max_expense
    interest_expense_scale = interest_expense / max_expense
    market_cap_scale = market_cap / max_expense

    ax.plot([-base_width / 2, base_width / 2], [0, 0], color='brown', lw=4) #base of the scale
    ax.plot([0, 0], [0, support_height], color='black', lw=4) #vertical line from the base to support height
    ax.plot([-beam_length / 2, beam_length / 2], [support_height, support_height], color='gray', lw=4) #horizontal beam on the support

    left_plate_x = -beam_length / 2 #determines where to place the revenue plate at the end of the beam
    ax.plot([left_plate_x, left_plate_x], [support_height, support_height - 2 * revenue_scale], color='blue', lw=4) #plots vertical line downward from the beam proportional to revenue_scale
    ax.text(left_plate_x, support_height - 2.5 * revenue_scale, f"Revenue: {revenue}", ha='center', color='blue') #places text below the revenue plate to display the revenue amount

    right_plate_x = beam_length / 2 #draws the right plate of the scale representing total expenses, scaled, and labeled total expenses
    ax.plot([right_plate_x, right_plate_x], [support_height, support_height - 2 * total_expense_scale], color='red', lw=4) #plots vertical line downward proportinal to total_expense_scale
    ax.text(right_plate_x, support_height - 2.5 * total_expense_scale, f"Total Expenses: {total_expenses}", ha='center', color='red') #places text label below the expense plate to display the total expenses amount

    max_tilt_angle_deg = 20 #max possible tilt of the scale
    difference = revenue - total_expenses #net difference between the revenue and expenes
    max_value = max(revenue, total_expenses) #get the max value
    # Calculate tilt angle in radians (already done earlier)
    tilt_angle_deg = (difference / max_value) * max_tilt_angle_deg
    tilt_angle = np.deg2rad(tilt_angle_deg) #convert to radians

    # Function to rotate points by a given angle around the origin
    def rotate_point(x, y, angle):
        x_rotated = x * np.cos(angle) - y * np.sin(angle)
        y_rotated = x * np.sin(angle) + y * np.cos(angle)
        return x_rotated, y_rotated

    # Stacked rectangles for expenses
    stack_x_position = right_plate_x + -1 #-1.5   Set the x coordinate slightly left of the expenses plate for stacking
    current_height = support_height + 1.60  # Starting y-coordinate above the beam for stacking rectangles

    # Rotate cost of revenue rectangle
    current_height -= 2 * cost_of_revenue_scale
    x0, y0 = rotate_point(stack_x_position, current_height, tilt_angle)
    ax.add_patch(plt.Rectangle((x0, y0), 1, 2 * cost_of_revenue_scale, color='orange'))
    ax.text(x0 + 0.5, y0 + cost_of_revenue_scale, f"Cost of Revenue: {cost_of_revenue}", ha='center', color='black')

    # Rotate operating expense rectangle
    current_height -= 2 * operating_expense_scale
    x1, y1 = rotate_point(stack_x_position, current_height, tilt_angle)
    ax.add_patch(plt.Rectangle((x1, y1), 1, 2 * operating_expense_scale, color='purple'))
    ax.text(x1 + 0.5, y1 + operating_expense_scale, f"Operating Expense: {operating_expense}", ha='center',
            color='black')

    # Rotate interest expense rectangle
    current_height -= 2 * interest_expense_scale
    x2, y2 = rotate_point(stack_x_position, current_height, tilt_angle)
    ax.add_patch(plt.Rectangle((x2, y2), 1, 2 * interest_expense_scale, color='green'))
    ax.text(x2 + 0.5, y2 + interest_expense_scale, f"Interest Expense: {interest_expense}", ha='center', color='black')

    # Rotate interest expense rectangle

    # Set the position for Total Revenue
    total_revenue_x_position = left_plate_x + .10  # This positions it on the left side of the scale
    current_revenue_height = support_height + 2  # Starting height for Total Revenue

    # Rotate total revenue rectangle
    current_revenue_height -= 2 * revenue_scale  # Decrement height for proper stacking
    x_total_revenue, y_total_revenue = rotate_point(total_revenue_x_position, current_revenue_height, tilt_angle)

    # Add the Total Revenue rectangle to the plot
    ax.add_patch(plt.Rectangle((x_total_revenue, y_total_revenue), 1, 2 * revenue_scale, color='blue'))
    ax.text(x_total_revenue + 0.5, y_total_revenue + revenue_scale, f"Total Revenue: {revenue}", ha='center',
            color='brown')
    # Market Cap visual on the left side of the screen
    market_cap_x_position = beam_length / 2 + 3 #setting the location of the market cap bar
    market_cap_y_position = support_height - 9

    # Market Cap changing value, everything involving a year
    ax.add_patch(plt.Rectangle((market_cap_x_position, market_cap_y_position), 1, 2 * market_cap_scale, color='green'))
    ax.text(market_cap_x_position + 0.5, market_cap_y_position + market_cap_scale, f"Market Cap: {market_cap}", ha='center',
            color='black')



    for line in ax.lines[-3:]: #selects the law three lines added, applies a rotation transformation to simulate the scale tilting toward the heavier side
        x_data, y_data = line.get_data()
        x_tilted = x_data * np.cos(tilt_angle) - y_data * np.sin(tilt_angle)
        y_tilted = x_data * np.sin(tilt_angle) + y_data * np.cos(tilt_angle)
        line.set_data(x_tilted, y_tilted)

    ax.set_xlim(-10, 10)
    ax.set_ylim(-5, 7)

    ax.text(0, -3, "Company Performance: Revenue vs. Expenses", ha='center', fontsize=16, fontweight='bold')
    ax.axis('off')
    ax.text(0, support_height + 2, f"Market Cap: ${market_cap:,.0f}", ha='center', color='green', fontsize=12, fontweight='bold')


def animate_scale(ticker, years): #animate the drawing of the financial scale based on the ticker and the years
    financial_data = [load_data(ticker, year) for year in years] #iterate through each year in the years list and call load_date function for each year
    fig, ax = plt.subplots(figsize=(25, 15)) #new figure and axes and setting the size

    def update(frame): #indexes the animation for the different years, dynamically updating the draw_scale function every time that you call this
        year = years[frame] #get the current year relative to the animation
        total_revenue, cost_of_revenue, operating_expense, interest_expense, market_cap = financial_data[frame] #unpacking financial metrics for the current year from financial_data baed on the frame index
        ax.clear()#clear the axis from any previous drawings
        draw_scale(ax, total_revenue, cost_of_revenue, operating_expense, interest_expense, market_cap) #redraw the scale on the axis
        ax.set_title(f"Financial Data for {year}") #setting the title of the plot to indicate which years information you are looking at

    ani = animation.FuncAnimation(fig, update, frames=len(years), repeat=True, interval=2000) #fig used to animate, update to call each frame, frames is the toal number of frames length of the years list, delay is 2 seconds

    plt.show()


ticker = 'AAPL' #the ticker that we want to see
years = ['2020', '2021', '2022', '2023'] #the list of years that we can get
animate_scale(ticker, years)
