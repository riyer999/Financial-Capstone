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

# Route for the homePage.html page
@app.route('/homePage')
def homePage():
    return render_template('homePage.html')

#route for about us
@app.route('/about')
def aboutUsPage():
    return render_template('aboutUsPage.html')



@app.route('/data/<ticker>') #defining a route for a web application. the /data/ticker is the url for the localhost, the ticker can be replaced with only tickers in the make_allData file
def get_data(ticker): #takes ticker as an argument. the value of the ticker will be passed to the url
    if ticker in allData: #is the ticker in the allData library??
        income_statement = allData[ticker]['income_statement'] #we just want income statement stuffs right now

        if 'Operating Expense' in income_statement.index: #check the operating expenses entry present in the income statement
            try: #catch potential errors
                operating_expenses = income_statement.loc['Operating Expense'] # extractes the operating expenses from the income statement
                cleaned_expenses = operating_expenses[operating_expenses != 0].dropna() #cleans the operating expenses by removing any entires that are zero and dropping the nan values
                expenses_list = cleaned_expenses.values.tolist() #was getting a problem with zeroes being displayed
                dates = cleaned_expenses.index.astype(str).tolist()

                plt.figure(figsize=(10, 5)) #actual plotting part
                plt.bar(dates, expenses_list, color='blue', width=0.4)
                plt.title(f'Operating Expenses for {ticker}')
                plt.xlabel('Dates')
                plt.ylabel('Operating Expenses')
                plt.xticks(rotation=45)
                plt.tight_layout()

                with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmpfile: #creating a temporary file to save the generated image.
                    plt.savefig(tmpfile.name) #saves the current figure to a temp file created in the prevous line
                    plt.close()  # Clear the figure to free up memory
                    return send_file(tmpfile.name, mimetype='image/png') #Sends the image back to the client
            except Exception as e:
                return f'Error generating plot: {str(e)}', 500
        else:
            return f'Operating Expenses not found for ticker {ticker}.', 404
    else:
        return f'Ticker "{ticker}" not found in the data.', 404

if __name__ == '__main__':
    app.run(debug=True)


