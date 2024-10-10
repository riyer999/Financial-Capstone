from flask import Flask, render_template, request, send_from_directory
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pickle
import pandas as pd
import yfinance as yf
import os

app = Flask(__name__, template_folder='frontend/templates')



def get_average_share_price(ticker, year):
    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"
    stock_data = yf.Ticker(ticker)
    historical_data = stock_data.history(start=start_date, end=end_date)
    average_price = historical_data['Close'].mean()
    return average_price


def load_data(ticker, year):
    with open('allData.pkl', 'rb') as file:
        allData = pickle.load(file)

    income_statement = allData[ticker]['income_statement']
    balance_sheet = allData[ticker]['balance_sheet']

    total_revenue = income_statement.loc['Total Revenue', year].item()
    gross_profit = income_statement.loc['Gross Profit', year].item()
    cost_of_revenue = total_revenue - gross_profit
    operating_expense = income_statement.loc['Operating Expense', year].item()
    interest_expense = income_statement.loc['Interest Expense', year].item()
    total_expenses = cost_of_revenue + operating_expense + interest_expense

    shares_outstanding = balance_sheet.loc['Ordinary Shares Number', year]
    if isinstance(shares_outstanding, pd.Series):
        shares_outstanding = shares_outstanding.iloc[0]

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


def animate_scale(ticker, years):
    financial_data = [load_data(ticker, year) for year in years]
    fig, ax = plt.subplots(figsize=(25, 15))

    def update(frame):
        year = years[frame]
        total_revenue, cost_of_revenue, operating_expense, interest_expense, market_cap = financial_data[frame]
        ax.clear()
        draw_scale(ax, total_revenue, cost_of_revenue, operating_expense, interest_expense, market_cap)
        ax.set_title(f"Financial Data for {year}")

    ani = animation.FuncAnimation(fig, update, frames=len(years), repeat=True, interval=2000)

    # Save as MP4
    output_path = f'static/videos/{ticker}_animation.mp4'
    ani.save(output_path, writer='ffmpeg', fps=30)

    plt.close(fig)  # Close the figure after saving to free memory
    return output_path


@app.route('/', methods=['GET', 'POST'])
def index():
    video_path = None
    if request.method == 'POST':
        ticker = request.form['ticker']
        years = ['2020', '2021', '2022', '2023']  # You can also make this dynamic if needed
        video_path = animate_scale(ticker, years)
    return render_template('index.html', video_path=video_path)


@app.route('/videos/<path:filename>')
def send_video(filename):
    return send_from_directory('static/videos', filename)


if __name__ == '__main__':
    app.run(debug=True)
