import pandas as pd
import numpy as np

r_df = pd.read_csv('data/Total Report.csv', sep=';', decimal=',')
for col in r_df.select_dtypes(include='object').columns:
    r_df[col] = r_df[col].str.strip()

bf = r_df[r_df['Machine'] == 'Biscuit Filling Machine'].copy()
bf['start'] = pd.to_datetime(bf['StartDateTime'], format='%d/%m/%y %H:%M')
bf = bf.sort_values('start').reset_index(drop=True)

print("=== BISCUIT FILLING MACHINE: FIRST 30 ROWS ===")
for i in range(30):
    r = bf.loc[i]
    print(f"Row {i:2} | {r['StartDateTime']} to {r['EndDateTime']} | dur:{r['Duration']:5.2f}m | total:{r['TotalBiscuitsMade']:7} | good:{r['GoodMadeBiscuits']:6} | cat:{r['OEE Category'][:10]} | prod:{r['Product']}")
