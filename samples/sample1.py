import numpy as np
import requests

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

print(f"Mean exchange rate: {mean_rate}")
print(f"Standard deviation of exchange rates: {std_dev_rate}")
