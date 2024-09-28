import numpy as np
import requests
from samples.sample_dir.sample_dir_1 import sample_function

# Fetch data from a URL
url = "https://api.exchangerate-api.com/v4/latest/USD"
response = requests.get(url)
data = response.json()

# Extract exchange rates
rates = data["rates"]

# Convert rates to a numpy array
rates_array = np.array(list(rates.values()))

# Perform some basic numpy operations
mean_rate = np.mean(rates_array)
std_dev_rate = np.std(rates_array)

# Perform sample self made function
sample_function()
