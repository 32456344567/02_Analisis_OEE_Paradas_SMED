import pandas as pd
import numpy as np

r_df = pd.read_csv('data/Total Report.csv', sep=';', decimal=',')
t_df = pd.read_csv('data/Target Speed.csv', sep=';')
p_df = pd.read_csv('data/Products.csv', sep=';')
m_df = pd.read_csv('data/Machine.csv', sep=';')

for df in [r_df, t_df, p_df, m_df]:
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].str.strip()

# Let's inspect how Challenge 18 DAX formulas were structured:
# In Enterprise DNA, they typically define:
# [Total Duration] = SUM('Total Report'[Duration])   (in minutes)
# [Run Time (min)] = CALCULATE(SUM('Total Report'[Duration]), 'Total Report'[OEE Category] = "Run Time")
# OR is Operating Time = Total Duration - CC - PM?
# Let's check what categories exist:
# 'Run Time', 'CC (Changeover Cleaning)', 'NO (No Order)', 'PM (Maintenance)', '0'

print("Sum of Duration (hours) by category across the whole dataset:")
dur_by_cat = r_df.groupby('OEE Category')['Duration'].sum() / 60
print(dur_by_cat)

print("\nSum of Duration by Machine and Category:")
pivot_dur = r_df.pivot_table(index='Machine', columns='OEE Category', values='Duration', aggfunc='sum', fill_value=0) / 60
print(pivot_dur)
