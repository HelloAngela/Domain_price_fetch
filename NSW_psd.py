# trimming NSW PSD data for analysis
import csv
import pandas as pd

with open("C:\\Users\\hello\\Desktop\\archive\\NSW_psd20221026_clean.csv") as f:
    df = pd.read_csv(f)
#
# df.fillna(0)
# df.replace('nan', 0)
# df.columns = df.columns.str.replace('[#,@,&]', '')
# df.astype()
# df.astype(columns[{'listing_id': 'int64'}])
# df2.astype({'listing_id': 'int64'})
# df.dtypes
# df.drop(['B', 'C'], axis='columns')
# df.columns = df.columns.str.replace(' ', '_')

locality = ['Ryde']
df_ryde = df[df['Property_locality' == "Ryde"]]
df.loc[df['column_name'].isin(some_values)]

# df.to_csv("C:\\Users\\hello\\Desktop\\archive\\NSW_psd20221026_clean.csv", index=False)