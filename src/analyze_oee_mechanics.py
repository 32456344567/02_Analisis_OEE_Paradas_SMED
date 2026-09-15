import pandas as pd
import numpy as np

r_df = pd.read_csv('data/Total Report.csv', sep=';', decimal=',')
for col in r_df.select_dtypes(include='object').columns:
    r_df[col] = r_df[col].str.strip()

print("=== TOTAL REPORT OVERVIEW ===")
print("Total rows:", len(r_df))

# Check columns
print("\nUnique OEE Categories:", r_df['OEE Category'].unique())

# Duration sum per category
cat_summary = r_df.groupby('OEE Category').agg(
    count=('Duration', 'count'),
    total_minutes=('Duration', 'sum'),
    total_biscuits=('TotalBiscuitsMade', 'sum'),
    good_biscuits=('GoodMadeBiscuits', 'sum')
)
cat_summary['total_hours'] = cat_summary['total_minutes'] / 60
cat_summary['pct_time'] = cat_summary['total_minutes'] / cat_summary['total_minutes'].sum() * 100
print("\nCategory Summary:")
print(cat_summary[['count', 'total_hours', 'pct_time', 'total_biscuits', 'good_biscuits']])

# Look closely at how machines log production
print("\nMachine breakdown of biscuits:")
m_summary = r_df.groupby('Machine').agg(
    rows=('Duration', 'count'),
    hours=('Duration', lambda x: x.sum() / 60),
    total_biscuits=('TotalBiscuitsMade', 'sum'),
    good_biscuits=('GoodMadeBiscuits', 'sum'),
    max_total_bisc=('TotalBiscuitsMade', 'max'),
    max_good_bisc=('GoodMadeBiscuits', 'max')
)
print(m_summary)
