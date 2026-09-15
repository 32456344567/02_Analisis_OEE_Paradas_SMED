import pandas as pd
import numpy as np

df = pd.read_csv('data/Total Report.csv', sep=';', decimal=',')
for col in df.select_dtypes(include='object').columns:
    df[col] = df[col].str.strip()

bf = df[df['Machine'] == 'Biscuit Filling Machine'].copy()
bf['delta_tot'] = bf['TotalBiscuitsMade'].diff()
bf['delta_good'] = bf['GoodMadeBiscuits'].diff()
bf['speed_total_bisc_h'] = (bf['delta_tot'] / bf['Duration']) * 60
bf['speed_good_bisc_h'] = (bf['delta_good'] / bf['Duration']) * 60

print("=== SPEED AND PRODUCTION BY OEE CATEGORY IN BISCUIT FILLING MACHINE ===")
for cat, g in bf.groupby('OEE Category'):
    valid = g[(g['delta_tot'] > 0) & (g['delta_tot'] < 100000)]  # exclude counter reset jumps
    mean_spd = valid['speed_total_bisc_h'].mean()
    med_spd = valid['speed_total_bisc_h'].median()
    tot_prod = valid['delta_tot'].sum()
    print(f"Category: {cat:25} | Rows: {len(g):4} | Rows with prod: {len(valid):4} | Total Prod: {tot_prod:10,.0f} | Median Speed: {med_spd:8,.0f} /h")
