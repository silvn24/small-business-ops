"""
This script was written for analysis of internal ERP export files in a small service
business context.

The script does not access live systems and includes no data. No identifying information is hardcoded in the script. 
The script references identifier columns expected in ERP export files; no data files are included.

This code is shared solely to demonstrate applied operations analysis in Python.
"""

import pandas as pd

s2022 = pd.read_excel('FileName1.xlsx')

# Combine three columns to create a new customer ID
s2022['customer_id'] = s2022['Customer'].astype(str) + '_' + s2022['ShipTo'].astype(str) +'_'+ s2022['RefNum']

selected_columns = ['customer_id', 'Partner', 'ApptStart', 'day_value', 'ApptDesc', 'SRODesc']
new_df_all = s2022[selected_columns]

#sample_data = new_df_all.iloc[1:15]
#print(sample_data)

# Group the DataFrame by customer id and count the frequency of each id
id_freq = new_df_all.groupby(['customer_id']).size().reset_index(name='total_count')

# Group the DataFrame by customer id, partner, day value, and count the frequency of each day value
freq_data = new_df_all.groupby(['customer_id', 'Partner', 'day_value']).size().reset_index(name='count')

# Find the day value that appears most frequently for each customer id
most_freq = freq_data.groupby(['customer_id'])['count'].idxmax()
most_freq_data = freq_data.loc[most_freq]

# Group the most frequent data by customer ID and day value and count the frequency of each partner
most_freq_partner = most_freq_data.groupby(['customer_id', 'day_value', 'Partner']).size().reset_index(name='count')

# Find the partner that appears most frequently for each customer id and day value combination
most_freq_partner = most_freq_partner.loc[most_freq_partner.groupby(['customer_id', 'day_value'])['count'].idxmax()]

# Merge the most frequent partner and total count dataframes
merged_data = pd.merge(most_freq_partner, id_freq, on='customer_id')


# Create a new DataFrame with the most frequent day value, most frequent partner and customer id columns
new_data = pd.DataFrame({'customer_id': merged_data['customer_id'].values,
                         'most frequent day': merged_data['day_value'].values,
                         'most frequent partner': merged_data['Partner'].values,
                         'total count': merged_data['total_count'].values})

new_data['custnum'] = new_data['customer_id'].str[:12]
new_data['refnum'] = new_data['customer_id'].str[12:]

# Write the new_data dataframe to an Excel file
with pd.ExcelWriter('FileName1_output.xlsx') as writer:
    new_data.to_excel(writer, sheet_name='freq_day', index=False)

# Print a confirmation message
print('Most frequent days for each customer ID written to Excel file.')
