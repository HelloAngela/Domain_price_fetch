# Adding the property prices to the property list csv
# Import libraries
import pandas as pd
import re
import csv
import pandas as pd

# def use_regex(input_text):
#     pattern = re.compile(r"Price range:\$\d\.\d-\$\d\.\d", re.IGNORECASE)
#     return pattern.match(input_text)


# Define regex objects
price_format = re.compile(r"\$\d\.\d-\$\d\.\d")

# Open and parse txt file

with open("C:\\Users\\hello\\Dropbox\\Python\\price_2111.txt") as text:
    price_list = text.read()
    price = re.findall(price_format, price_list)

print(price)

list1 = price[0:36]
list2 = price[36:80]

print(list1)
print(list2)


# csv_input = pd.read_csv("C:\\Users\\hello\\Dropbox\\Python\\property_list_test.csv")
# csv_input['property.price'] = pd.Series(list1)
# csv_input = csv_input.fillna(0)

# with open("C:\\Users\\hello\\Dropbox\\Python\\property_list_test.csv") as f:
#     csv_input = pd.read_csv(f)
#     csv_input['property.price'] = pd.Series(list1)
#     csv_input = csv_input.fillna(0)
#     csv_input.to_csv("C:\\Users\\hello\\Dropbox\\Python\\property_list_test.csv", index=False)

with open("C:\\Users\\hello\\Dropbox\\Python\\property_list_2122_filt.csv") as f2:
    csv_input2 = pd.read_csv(f2)
    csv_input2['property.price'] = pd.Series(list2)
    csv_input2 = csv_input2.fillna(0)
    csv_input2.to_csv("C:\\Users\\hello\\Dropbox\\Python\\property_list_2122_filt.csv", index=False)
