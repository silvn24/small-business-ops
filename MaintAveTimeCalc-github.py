"""
This script was written for analysis of internal ERP export files in a small service
business context.

The script does not access live systems and includes no data. The script references 
identifier columns expected in ERP export files; no data or identifiers are included 
in this repository. Any numeric values in the script are placeholder values and do 
not reflect actual pricing, service durations, or operational parameters used by the business.

This code is shared solely to demonstrate applied operations analysis in Python.
"""

import pandas as pd
from datetime import datetime, timedelta

df_visits = pd.read_excel('Maint_dummy_data.xlsx') #Use sample dummy data or replace the file name with your own

# Combine two columns to create a new customer ID (customer number plus ship to)
df_visits['customer_id'] = df_visits['Customer'].astype(str) + '_' + df_visits['ShipTo'].astype(str)

#print(df_visits.head)

#selecting specific columns and creating a new df
selected_columns = ['customer_id', 'SRO', 'StartDate', 'EndDate', 'Item', 'TransDate', 'ExtPrice']

new_df_visits = df_visits[selected_columns]

#removing records with an empty cell and any chem check visits
df_visits_cln = new_df_visits.dropna().loc[new_df_visits['Item'] != 5]

#calculating total visit time enddate-startdate/24
df_visits_cln['visit_time'] = (df_visits_cln['EndDate'] - df_visits_cln['StartDate']).dt.total_seconds() / 3600

#group by customer id
df_visits_cln = df_visits_cln.sort_values(['customer_id', 'Item', 'TransDate'])

ave_visit_time = df_visits_cln.groupby(['customer_id','Item'])['visit_time'].mean()

item_count = df_visits_cln.groupby(['customer_id', 'Item']).size()

# Get the most recent ExtPrice for each customer and visit type
most_recent_price = df_visits_cln.groupby(['customer_id', 'Item'])['ExtPrice'].last()

# Reset the index to convert the resulting Series to a DataFrame
ave_result = ave_visit_time.reset_index()

# Add the visit type count column to the result DataFrame
ave_result['Item_count'] = item_count.values

# Merge with original DataFrame to include pricing and most recent rate
ave_result = pd.merge(ave_result, df_visits_cln[['customer_id', 'Item', 'TransDate']], on=['customer_id', 'Item'], how='left')
ave_result = pd.merge(ave_result, most_recent_price, on=['customer_id', 'Item'], how='left')

#calculate minutes over/under visit allowance; 0.67 represents the expected visit duration
ave_result['Over_Under'] = (ave_result['visit_time']) - 0.67


# Drop duplicates to keep only one entry per customer per visit type
ave_result = ave_result.drop_duplicates(subset=['customer_id', 'Item'])

ave_result = ave_result.reindex(columns=['customer_id', 'Item', 'Item_count', 'ExtPrice', 'visit_time', 'Over_Under'])

#calculate adjusted price according to average time spent
#price divided by expected max visit length in minutes times actual visit time (converted from decimal time to minutes)
ave_result['Corrected_price'] = (ave_result['ExtPrice'] / 50) * (ave_result['visit_time'] * 60)

#calculate profit loss between old price and adjusted price
ave_result['Profit_Loss'] = (ave_result['ExtPrice'] - ave_result['Corrected_price'])

# Write the DataFrame to an Excel file
ave_result.to_excel('output_Maint_dummy_data.xlsx', index=False)
