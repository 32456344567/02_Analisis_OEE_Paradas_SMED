import pandas as pd

r_df = pd.read_csv('data/Total Report.csv', sep=';', decimal=',')
for col in r_df.select_dtypes(include='object').columns:
    r_df[col] = r_df[col].str.strip()

bf = r_df[r_df['Machine'] == 'Biscuit Filling Machine'].copy()
bf['start'] = pd.to_datetime(bf['StartDateTime'], format='%d/%m/%y %H:%M')
bf['end'] = pd.to_datetime(bf['EndDateTime'], format='%d/%m/%y %H:%M')
bf = bf.sort_values('start').reset_index(drop=True)

# Check gaps between end of row i and start of row i+1
bf['gap_to_next'] = (bf['start'].shift(-1) - bf['end']).dt.total_seconds() / 60
print("Gaps to next event stats (minutes):")
print(bf['gap_to_next'].describe())
print("\nNumber of gaps > 5 minutes:", (bf['gap_to_next'] > 5).sum())
print("Total sum of positive gaps (hours):", bf[bf['gap_to_next'] > 0]['gap_to_next'].sum() / 60)
print("Top 10 largest gaps:")
print(bf.nlargest(10, 'gap_to_next')[['StartDateTime', 'EndDateTime', 'gap_to_next', 'OEE Category', 'Product']])
