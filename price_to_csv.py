# Adding the property prices to the property list csv
# Import libraries
import pandas as pd
import re

# Define regex objects
price_format = re.compile('\d')

# Open and parse txt file

with open("C:\\Users\\hello\\Dropbox\\Python\\price_2111.txt") as price_list:
    price = price_format.search(str(price_list))

print(price)
