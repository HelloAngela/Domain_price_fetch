# Filter listing.csv based on what's already on file. Because there's a daily token limit for API

import pandas as pd
import csv


with open("C:\\Users\\hello\\Dropbox\\Python\\property_list_261022.csv") as f:
    df = pd.read_csv(f)

with open("C:\\Users\\hello\\Dropbox\\Python\\property_list_combined.csv") as f2:
    df_combo = pd.read_csv(f2)

# Filter df with df_combo, only retaining df rows NOT IN df_combo (unsearched listings)
df1 = df[~df.listing_id.isin(df_combo.listing_id)]
df1.to_csv("C:\\Users\\hello\\Dropbox\\Python\\property_list_261022_filt.csv", index=False)


