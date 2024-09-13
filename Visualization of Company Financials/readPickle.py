import pickle

# Load the data from the pickle file
with open('allData.pkl', 'rb') as file:
    allData = pickle.load(file)

# Example: Print data for coca cola
print(allData['KO'])