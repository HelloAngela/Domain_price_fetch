# Originally developed by Alex D'Ambra
# Import libraries
import json
import requests  # request library: http://docs.python-requests.org/en/master/
import re, string, timeit
import time
import pandas as pd
from os.path import abspath

# creating list for upper and lower price range
upper_l = []
lower_l = []

# Define guess price function


def guess_price(i):
    # Search parameters, property ID available from end of domain URL.
    # Set starting lower bound (starting_max_price), starting min price is lower bound plus 400k.
    starting_max_price = 1700000
    increment = 100000
    # when starting min price is zero we'll just use the lower bound plus 400k later on
    starting_min_price = 0

    # POST request to receive token. Required: client_id and client_secret
    # client_95192f1059f951a8eb2c3e9a9d1161ec
    # secret_ce1de517c47c4fd80ac0658ae986ab3f
    # client_10873b37e3a0218aa7f1c4fb779684bd
    # secret_bd3af3a039426e1cdfca319c032218ab
    # client_ebfa37bc599d11e0405c1c9cfaa925c6
    # secret_3d310ee2180c109dc66d882ecc0cb488

    response = requests.post('https://auth.domain.com.au/v1/connect/token',
                             data={'client_id': 'client_95192f1059f951a8eb2c3e9a9d1161ec',
                                   "client_secret": "secret_ce1de517c47c4fd80ac0658ae986ab3f",
                                   "grant_type": "client_credentials", "scope": "api_listings_read",
                                   "Content-Type": "text/json"})
    token = response.json()
    access_token = token["access_token"]



    # GET Request for ID, make a GET request to the listings endpoint to retrieve listing info based on property ID.
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
        # denom = "k"
    else:
        lower = max_price / 1000000
        upper = min_price / 1000000
        # denom = "m"

        upper_l.append(upper)
        lower_l.append(lower)


    # Print results

    # print(da['displayAddress'])
    # print(r['headline'])
    # print("Property Type:", property_type_str)
    # print("Details: ", int(bedrooms), "bedroom,", int(bathrooms), "bathroom,", int(carspaces), "carspace")
    # print("Display price:", r['priceDetails']['displayPrice'])
    # if max_price == min_price:
    #     print("Price guide:", "$", lower, denom)
    # else:
    #     print("Price range:", "$", lower, "-", "$", upper, denom)
    # print("URL:", r['seoUrl'])

    # Output results to txt

    # with open("C:\\Users\\hello\\Dropbox\\Python\\price_2111.txt", 'a') as f:
    #     f1 = da['displayAddress']
    #     f2 = '\n' + r['headline']
    #     f3 = '\n' +"Property Type:" + property_type_str
    #     f4 = '\n' +"Details: " + str(int(bedrooms)) + " bedroom," + str(int(bathrooms)) + " bathroom," + str(int(carspaces)) + " carspace"
    #     f5 = '\n' +"Display price:" + r['priceDetails']['displayPrice']
    #     if max_price == min_price:
    #          f6 = '\n' + "Price guide:"+ "$"+ str(lower)+ denom
    #     else:
    #          f6 = '\n' + "Price range:"+ "$"+ str(lower)+ "-"+ "$"+ str(upper)+ denom
    #     f7 = '\n' + "URL:" + r['seoUrl']
    #     f.writelines([f1, f2, f3, f4, f5, f6, f7])
    #
# Get ID list from csv


df1 = pd.read_csv("C:\\Users\\hello\\Dropbox\\Python\\property_list_261022_filt.csv")
ID_list = list((df1['listing_id']))

for i in ID_list:
    property_id = str(i)
    guess_price(property_id)

# adding the newly generated price list to dataframe, and save as csv
df1['upper_bound'] = upper_l
df1['lower_bound'] = lower_l
df1.to_csv("C:\\Users\\hello\\Dropbox\\Python\\property_list_261022_parsed.csv", index=False)

