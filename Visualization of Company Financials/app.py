from flask import Flask, render_template, send_file #flask is the web framework used for making the web server
import pickle #used to load serialized data. the data stored in allData.pkl
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Set to non-GUI backend
import matplotlib.pyplot as plt
import tempfile

app = Flask(__name__, template_folder='frontend/templates') #this argument specifies where flask will look for the html file to render. its looking for the html fles in the frontend/templates directory

# Load data from the pickle file
with open('backend/allData.pkl', 'rb') as file:  #opens the allData.pkl containing the financial information stored
    allData = pickle.load(file) #reads in the pickle data from the allData.pkl

# Define a route for the home page
@app.route('/') #defines a route (URL) for the root of the web application.
def home(): #logic that runs when the home route is accessed
    return render_template('index.html') #returns and renders the index.html page


# Define a route to serve the Operating Expenses data as a plot
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data/<ticker>')
def get_data(ticker):
    if ticker in allData:
        income_statement = allData[ticker]['income_statement']

        if 'Operating Expense' in income_statement.index:
            try:
                operating_expenses = income_statement.loc['Operating Expense']
                cleaned_expenses = operating_expenses[operating_expenses != 0].dropna()
                expenses_list = cleaned_expenses.values.tolist()
                dates = cleaned_expenses.index.astype(str).tolist()

                plt.figure(figsize=(10, 5))
                plt.bar(dates, expenses_list, color='blue', width=0.4)
                plt.title(f'Operating Expenses for {ticker}')
                plt.xlabel('Dates')
                plt.ylabel('Operating Expenses')
                plt.xticks(rotation=45)
                plt.tight_layout()

                with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmpfile:
                    plt.savefig(tmpfile.name)
                    plt.close()  # Clear the figure to free up memory
                    return send_file(tmpfile.name, mimetype='image/png')
            except Exception as e:
                return f'Error generating plot: {str(e)}', 500
        else:
            return f'Operating Expenses not found for ticker {ticker}.', 404
    else:
        return f'Ticker "{ticker}" not found in the data.', 404

if __name__ == '__main__':
    app.run(debug=True)