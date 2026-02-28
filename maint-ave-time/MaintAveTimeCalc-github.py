"""
This script was written for analysis of internal ERP export files in a small service
business context.

The script does not access live systems and no data is hard coded. The script references 
identifier columns expected in ERP export files; no data or identifiers are included 
in this repository. Any numeric values in the script are placeholder values and do 
not reflect actual pricing, service durations, or operational parameters used by the business.

This code is shared solely to demonstrate applied operations analysis in Python.
"""

import pandas as pd
from datetime import datetime, timedelta

df_visits = pd.read_excel('Maint_dummy_data.xlsx') #Use sample dummy data or replace the file name with your own

# Combine two columns to create a new customer ID (customer number plus sub-location [SubLoc)
df_visits['customer_id'] = df_visits['Customer'].astype(str) + '_' + df_visits['SubLoc'].astype(str)

#print(df_visits.head)

#selecting specific columns and creating a new df
selected_columns = ['customer_id', 'Order', 'StartDate', 'EndDate', 'WorkCode', 'PostedDate', 'Price']

new_df_visits = df_visits[selected_columns]

#removing records with an empty cell and any chem check visits
df_visits_cln = new_df_visits.dropna().loc[new_df_visits['WorkCode'] != 5]

#calculating total visit time enddate-startdate/24
df_visits_cln['visit_time'] = (df_visits_cln['EndDate'] - df_visits_cln['StartDate']).dt.total_seconds() / 3600

#group by customer id
df_visits_cln = df_visits_cln.sort_values(['customer_id', 'WorkCode', 'PostedDate'])

ave_visit_time = df_visits_cln.groupby(['customer_id','WorkCode'])['visit_time'].mean()

item_count = df_visits_cln.groupby(['customer_id', 'WorkCode']).size()

# Get the most recent Price for each customer and visit type
most_recent_price = df_visits_cln.groupby(['customer_id', 'WorkCode'])['Price'].last()

most_recent_posted = df_visits_cln.groupby(['customer_id', 'WorkCode'])['PostedDate'].last()

# Reset the index to convert the resulting Series to a DataFrame
ave_result = ave_visit_time.reset_index()

#Add the visit type count column (key-aligned)
ave_result = ave_result.merge(item_count.rename('Item_count').reset_index(), on=['customer_id', 'WorkCode'], how='left')

#Add most recent posted date (latest)
ave_result = ave_result.merge(most_recent_posted.rename('MostRecentPostedDate').reset_index(), on=['customer_id', 'WorkCode'], how='left')

ave_result = ave_result.merge(most_recent_price.rename('Price').reset_index(), on=['customer_id', 'WorkCode'], how='left')

#calculate hours over/under visit allowance; 0.70 (hours) represents the expected visit duration in decimal time. Again, this is a placeholder value and does not reflect the real world expected visit length of the business.
ave_result['Over_Under'] = (ave_result['visit_time']) - 0.70

ave_result = ave_result.reindex(columns=['customer_id', 'WorkCode', 'Item_count', 'MostRecentPostedDate', 'Price', 'visit_time', 'Over_Under'])

#calculate adjusted price according to default price per minute for expected default visit length, 60 minutes to convert visit hours (decimal time) to minutes
default_price = 58
default_minutes = 42
ave_result['TimeNormalizedPrice'] = (default_price / default_minutes) * (ave_result['visit_time'] * 60)

#calculate price variance
ave_result['PricingVariance'] = (ave_result['Price'] - ave_result['TimeNormalizedPrice'])

# Write the DataFrame to an Excel file
ave_result.to_excel('output_Maint_dummy_data.xlsx', index=False)
