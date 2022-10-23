# Originally developed by Alex D'Ambra
# Import libraries
import json
import requests  # request library: http://docs.python-requests.org/en/master/
import re, string, timeit
import time

# Search parameters, property ID available from end of domain URL eg.
# https://www.domain.com.au/132a-prince-edward-avenue-earlwood-nsw-2206-2014925785
# Set starting lower bound (500k), starting min price is lower bound plus 400k.
# Increment values

property_id = "2018145822"
starting_max_price = 1500000
increment = 100000
# when starting min price is zero we'll just use the lower bound plus 400k later on
starting_min_price = 0

# POST request to receive token. Required: client_id and client_secret

response = requests.post('https://auth.domain.com.au/v1/connect/token',
                         data={'client_id': 'client_10873b37e3a0218aa7f1c4fb779684bd',
                               "client_secret": "secret_bd3af3a039426e1cdfca319c032218ab",
                               "grant_type": "client_credentials", "scope": "api_listings_read",
                               "Content-Type": "text/json"})
token = response.json()
access_token = token["access_token"]

# GET Request for ID, make a GET request to the listings endpoint to retrieve listing info based on prperty ID.
url = "https://api.domain.com.au/v1/listings/" + property_id
auth = {"Authorization": "Bearer " + access_token}
request = requests.get(url, headers=auth)
r = request.json()

# Extract property details

da = r['addressParts']
postcode = da['postcode']
suburb = da['suburb']
bathrooms = r['bathrooms']
bedrooms = r['bedrooms']
carspaces = r['carspaces']
property_type = r['propertyTypes']
print(property_type, postcode, suburb, bedrooms, bathrooms, carspaces)

# the below puts all relevant property types into a single string. eg. a property listing can be a
# 'house' and a 'townhouse'
n = 0
property_type_str = ""
for p in r['propertyTypes']:
    property_type_str = property_type_str + (r['propertyTypes'][int(n)])
    n = n + 1
print(property_type_str)

# Looping through a series of POST requests starting with starting_max_price plus increment until we have a hit.
# If hit, then check if property of interest (ID) is in that list.
# Achieved by using a do while loop.


max_price = starting_max_price
searching_for_price = True

# Start POST loop for starting max price
while searching_for_price:

    url = "https://api.domain.com.au/v1/listings/residential/_search"  # Set destination URL here
    post_fields = {
        "listingType": "Sale",
        "maxPrice": max_price,
        "pageSize": 100,
        "propertyTypes": property_type,
        "minBedrooms": bedrooms,
        "maxBedrooms": bedrooms,
        "minBathrooms": bathrooms,
        "maxBathrooms": bathrooms,
        "locations": [
            {
                "state": "",
                "region": "",
                "area": "",
                "suburb": suburb,
                "postCode": postcode,
                "includeSurroundingSuburbs": False
            }
        ]
    }

    request = requests.post(url, headers=auth, json=post_fields)

    l = request.json()
    listings = []
    for listing in l:
        listings.append(listing["listing"]["id"])
    listings

    if int(property_id) in listings:
        max_price = max_price - increment
        print("Lower bound found: ", max_price)
        searching_for_price = False
    else:
        max_price = max_price + increment
        print("Not found. Increasing max price to ", max_price)
        time.sleep(0.1)  # sleep a bit so you don't make too many API calls too quickly

# Lower limit found, now another loop for upper bound, beginning with starting min price minus increment.

searching_for_price = True
if starting_min_price > 0:
    min_price = starting_min_price
else:
    min_price = max_price + 400000

while searching_for_price:

    url = "https://api.domain.com.au/v1/listings/residential/_search"  # Set destination URL here
    post_fields = {
        "listingType": "Sale",
        "minPrice": min_price,
        "pageSize": 100,
        "propertyTypes": property_type,
        "minBedrooms": bedrooms,
        "maxBedrooms": bedrooms,
        "minBathrooms": bathrooms,
        "maxBathrooms": bathrooms,
        "locations": [
            {
                "state": "",
                "region": "",
                "area": "",
                "suburb": suburb,
                "postCode": postcode,
                "includeSurroundingSuburbs": False
            }
        ]
    }

    request = requests.post(url, headers=auth, json=post_fields)

    l = request.json()
    listings = []
    for listing in l:
        listings.append(listing["listing"]["id"])
    listings

    if int(property_id) in listings:
        min_price = min_price + increment
        print("Upper bound found: ", min_price)
        searching_for_price = False
    else:
        min_price = min_price - increment
        print("Not found. Decreasing min price to ", min_price)
        time.sleep(0.1)  # sleep a bit so you don't make too many API calls too quickly

# Formatting output

if max_price < 1000000:
    lower = max_price / 1000
    upper = min_price / 1000
    denom = "k"
else:
    lower = max_price / 1000000
    upper = min_price / 1000000
    denom = "m"

# Print results

print(da['displayAddress'])
print(r['headline'])
print("Property Type:", property_type_str)
print("Details: ", int(bedrooms), "bedroom,", int(bathrooms), "bathroom,", int(carspaces), "carspace")
print("Display price:", r['priceDetails']['displayPrice'])
if max_price == min_price:
    print("Price guide:", "$", lower, denom)
else:
    print("Price range:", "$", lower, "-", "$", upper, denom)
print("URL:", r['seoUrl'])
