from flask import Flask, render_template, send_file, abort
import pickle
import matplotlib
import tempfile
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pandas as pd
import yfinance as yf
import os

app = Flask(__name__, template_folder='frontend/templates')

# Load data from the pickle file
with open('allData.pkl', 'rb') as file:
    allData = pickle.load(file)

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

    shares_outstanding = balance_sheet.loc['Ordinary Shares Number', year]
    if isinstance(shares_outstanding, pd.Series):
        shares_outstanding = shares_outstanding.iloc[0]

    average_share_price = get_average_share_price(ticker, year)
    market_cap = average_share_price * shares_outstanding
    return total_revenue, cost_of_revenue, operating_expense, interest_expense, market_cap

def draw_scale(ax, revenue, cost_of_revenue, operating_expense, interest_expense, market_cap):
    base_width = 6
    base_height = 1
    beam_length = 12
    support_height = 3

    total_expenses = cost_of_revenue + operating_expense + interest_expense
    max_expense = max(total_expenses, revenue)
    revenue_scale = revenue / max_expense
    total_expense_scale = total_expenses / max_expense
    cost_of_revenue_scale = cost_of_revenue / max_expense
    operating_expense_scale = operating_expense / max_expense
    interest_expense_scale = interest_expense / max_expense
    market_cap_scale = market_cap / max_expense

    ax.plot([-base_width / 2, base_width / 2], [0, 0], color='brown', lw=4)
    ax.plot([0, 0], [0, support_height], color='black', lw=4)
    ax.plot([-beam_length / 2, beam_length / 2], [support_height, support_height], color='gray', lw=4)

    left_plate_x = -beam_length / 2
    ax.plot([left_plate_x, left_plate_x], [support_height, support_height - 2 * revenue_scale], color='blue', lw=4)
    ax.text(left_plate_x, support_height - 2.5 * revenue_scale, f"Revenue: {revenue}", ha='center', color='blue')

    right_plate_x = beam_length / 2
    ax.plot([right_plate_x, right_plate_x], [support_height, support_height - 2 * total_expense_scale], color='red', lw=4)
    ax.text(right_plate_x, support_height - 2.5 * total_expense_scale, f"Total Expenses: {total_expenses}", ha='center', color='red')

    max_tilt_angle_deg = 20
    difference = revenue - total_expenses
    max_value = max(revenue, total_expenses)
    tilt_angle_deg = (difference / max_value) * max_tilt_angle_deg
    tilt_angle = np.deg2rad(tilt_angle_deg)

    def rotate_point(x, y, angle):
        x_rotated = x * np.cos(angle) - y * np.sin(angle)
        y_rotated = x * np.sin(angle) + y * np.cos(angle)
        return x_rotated, y_rotated

    stack_x_position = right_plate_x - 1
    current_height = support_height + 1.60

    current_height -= 2 * cost_of_revenue_scale
    x0, y0 = rotate_point(stack_x_position, current_height, tilt_angle)
    ax.add_patch(plt.Rectangle((x0, y0), 1, 2 * cost_of_revenue_scale, color='orange'))
    ax.text(x0 + 0.5, y0 + cost_of_revenue_scale, f"Cost of Revenue: {cost_of_revenue}", ha='center', color='black')

    current_height -= 2 * operating_expense_scale
    x1, y1 = rotate_point(stack_x_position, current_height, tilt_angle)
    ax.add_patch(plt.Rectangle((x1, y1), 1, 2 * operating_expense_scale, color='purple'))
    ax.text(x1 + 0.5, y1 + operating_expense_scale, f"Operating Expense: {operating_expense}", ha='center', color='black')

    current_height -= 2 * interest_expense_scale
    x2, y2 = rotate_point(stack_x_position, current_height, tilt_angle)
    ax.add_patch(plt.Rectangle((x2, y2), 1, 2 * interest_expense_scale, color='green'))
    ax.text(x2 + 0.5, y2 + interest_expense_scale, f"Interest Expense: {interest_expense}", ha='center', color='black')

    total_revenue_x_position = left_plate_x + .10
    current_revenue_height = support_height + 2

    current_revenue_height -= 2 * revenue_scale
    x_total_revenue, y_total_revenue = rotate_point(total_revenue_x_position, current_revenue_height, tilt_angle)
    ax.add_patch(plt.Rectangle((x_total_revenue, y_total_revenue), 1, 2 * revenue_scale, color='blue'))
    ax.text(x_total_revenue + 0.5, y_total_revenue + revenue_scale, f"Total Revenue: {revenue}", ha='center', color='brown')

    market_cap_x_position = beam_length / 2 + 3
    market_cap_y_position = support_height - 9

    ax.add_patch(plt.Rectangle((market_cap_x_position, market_cap_y_position), 1, 2 * market_cap_scale, color='green'))
    ax.text(market_cap_x_position + 0.5, market_cap_y_position + market_cap_scale, f"Market Cap: {market_cap}", ha='center', color='black')

    for line in ax.lines[-3:]:
        x_data, y_data = line.get_data()
        x_tilted = x_data * np.cos(tilt_angle) - y_data * np.sin(tilt_angle)
        y_tilted = x_data * np.sin(tilt_angle) + y_data * np.cos(tilt_angle)
        line.set_data(x_tilted, y_tilted)

    ax.set_xlim(-10, 10)
    ax.set_ylim(-5, 7)

    ax.text(0, -3, "Company Performance: Revenue vs. Expenses", ha='center', fontsize=16, fontweight='bold')
    ax.axis('off')
    ax.text(0, support_height + 2, f"Market Cap: ${market_cap:,.0f}", ha='center', color='green', fontsize=12, fontweight='bold')

def animate_scale(ticker, years):
    financial_data = [load_data(ticker, year) for year in years]
    fig, ax = plt.subplots(figsize=(25, 15))

    def update(frame):
        year = years[frame]
        total_revenue, cost_of_revenue, operating_expense, interest_expense, market_cap = financial_data[frame]
        ax.clear()
        draw_scale(ax, total_revenue, cost_of_revenue, operating_expense, interest_expense, market_cap)
        ax.set_title(f"Financial Data for {year}")

    anim = animation.FuncAnimation(fig, update, frames=len(years), repeat=True, interval=2000)
    matplotlib.rcParams['animation.ffmpeg_path'] = "C:\\Users\\RIyer\\Downloads\\ffmpeg-7.1-essentials_build\\ffmpeg-7.1-essentials_build\\bin\\ffmpeg.exe"
    video_path = f'static/videos/{ticker}_Moving_Scale.mp4'  # Save the video in the static folder
    writer = animation.FFMpegWriter(fps=1, metadata=dict(artist='Me'), bitrate=1800)
    anim.save(video_path, writer=writer)
    plt.close(fig)  # Close the figure after saving

    return video_path  # Return the path to the generated video

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data/<ticker>')
def get_data(ticker):
    years = ['2020','2021','2022', '2023']  # Example years
    video_path = animate_scale(ticker, years)
    return send_file(video_path)  # Return the video file as a response

if __name__ == '__main__':
    # Ensure the static/videos directory exists
    if not os.path.exists('static/videos'):
        os.makedirs('static/videos')
    app.run(debug=True)
