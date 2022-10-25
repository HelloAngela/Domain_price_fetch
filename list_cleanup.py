# Flattening json to csv

from csv import DictReader

# open file in read mode
with open("C:\\Users\\hello\\Dropbox\\Python\\property_list_test.csv", 'r') as f:
    dict_reader = DictReader(f)
    print(str(dict_reader))


# dict_variable = {key:value for (key,value) in dictonary.items()}
