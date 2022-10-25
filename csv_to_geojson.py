# Converting property listing csv to geojson for dash app.

import pandas as pd
import json

# Load .csv to dataframe, selecting columns to import
df = pd.read_csv("C:\\Users\\hello\\Dropbox\\Python\\property_list_test.csv",
                 usecols=['listing.id',
                          'listing.propertyDetails.propertyType',
                          'listing.propertyDetails.bathrooms',
                          'listing.propertyDetails.bedrooms',
                          'listing.propertyDetails.carspaces',
                          'listing.propertyDetails.latitude',
                          'listing.propertyDetails.longitude'
                          ])

# print(df)
# print(df.dtypes)

# converting data frame to json
json_result_string = df.to_json(
    orient='records',
    double_precision=12,
)
json_result = json.loads(json_result_string) # load() takes a file object and returns the json object.

# converting json to geojson
geojson = {
    'type': 'FeatureCollection',
    'features': []
}
for record in json_result:
    geojson['features'].append({
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': [record['listing.propertyDetails.longitude'], record['listing.propertyDetails.latitude']],
        },
        'properties': record,
    })

# dump json string into geojson
with open("C:\\Users\\hello\\Dropbox\\Python\\property_map.json", 'w') as f:
    f.write(json.dumps(geojson, indent=2))

