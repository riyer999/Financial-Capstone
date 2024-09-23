from flask import Flask, render_template
import pickle

app = Flask(__name__, template_folder='frontend/templates')

# Load data from the pickle file
with open('backend/allData.pkl', 'rb') as file:
    allData = pickle.load(file)

# Define a route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Define a route to serve the income statement data as a string
@app.route('/data/<ticker>')
def get_data(ticker):
    if ticker in allData:
        income_statement = allData[ticker]['income_statement']
        # Convert the income statement to a string representation
        income_statement_str = income_statement.to_string() if hasattr(income_statement, 'to_string') else str(income_statement)
        return income_statement_str  # Return as plain text
    else:
        return f'Ticker "{ticker}" not found in the data.', 404

if __name__ == '__main__':
    app.run(debug=True)
