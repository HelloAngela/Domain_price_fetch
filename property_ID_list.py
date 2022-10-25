# Retrieve a list of property IDs matching description, and output it on a txt.

# Import libraries
import requests
import json
import pandas as pd

# POST request to receive token
response = requests.post(url='https://auth.domain.com.au/v1/connect/token',
                         data={'client_id': 'client_10873b37e3a0218aa7f1c4fb779684bd',
                               "client_secret": "secret_bd3af3a039426e1cdfca319c032218ab",
                               "grant_type": "client_credentials", "scope": "api_listings_read",
                               "Content-Type": "text/json"})
auth_response = response.json()
access_token = auth_response["access_token"]


# Define search parameters
post_fields = {
        "listingType": "Sale",
        "minPrice": 1500000,
        "maxPrice": 4000000,
        "pageSize": 100,
        "propertyType": "house",
        "minBedrooms": 3,
        "maxBedrooms": 7,
        "minBathrooms": 2,
        "maxBathrooms": 4,
        "locations": [
            {
                "state": "NSW",
                "region": "",
                "area": "",
                "suburb": "Marsfield",
                "postCode": 2122,
                "includeSurroundingSuburbs": True
            }
        ]

}

# POST request for a list of property IDs
url = "https://api.domain.com.au/v1/listings/residential/_search"
auth = {"Authorization": "Bearer " + access_token}
request = requests.post(url, headers=auth, json=post_fields)
hits = request.json()

with open("C:\\Users\\hello\\Dropbox\\Python\\property_list.json", 'w') as search_result:
    search_result.write(json.dumps(hits))
# print(hits)

# Converting json to dataframe
with open("C:\\Users\\hello\\Dropbox\\Python\\property_list.json", 'r') as f:
    data = json.load(f)

df2 = pd.json_normalize(data, max_level=7)
df2.to_csv("C:\\Users\\hello\\Dropbox\\Python\\property_list_2122.csv")
