import pandas as pd
import numpy as np

r_df = pd.read_csv('data/Total Report.csv', sep=';', decimal=',')
for col in r_df.select_dtypes(include='object').columns:
    r_df[col] = r_df[col].str.strip()

bf = r_df[r_df['Machine'] == 'Biscuit Filling Machine'].copy()
print("Ratio Good/Total in individual rows:")
ratios = bf['GoodMadeBiscuits'] / bf['TotalBiscuitsMade'].replace(0, np.nan)
print(ratios.describe())
print("\nSample 10 ratios:")
for i in range(10):
    t = bf.iloc[i]['TotalBiscuitsMade']
    g = bf.iloc[i]['GoodMadeBiscuits']
    print(f"Row {i}: Total={t:7d}, Good={g:6d}, Ratio={g/t if t>0 else 0:.4f}, Cat={bf.iloc[i]['OEE Category']}")
