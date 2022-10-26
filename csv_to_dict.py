# converting csv to list of dict for use in app.py
from csv import DictReader

# open file in read mode
with open("C:\\Users\\hello\\Dropbox\\Python\\property_list_2111.csv", 'r') as f:
    dict_reader = DictReader(f)

    list_of_dict = list(dict_reader)

    print(list_of_dict)