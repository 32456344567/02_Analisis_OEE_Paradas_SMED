import pandas as pd
import numpy as np

r_df = pd.read_csv('data/Total Report.csv', sep=';', decimal=',')
for col in r_df.select_dtypes(include='object').columns:
    r_df[col] = r_df[col].str.strip()

t_df = pd.read_csv('data/Target Speed.csv', sep=';')
for col in t_df.select_dtypes(include='object').columns:
    t_df[col] = t_df[col].str.strip()

# Check Target speed: 51,840 or 43,200 biscuits/hour
# In 744 hours (1 month), maximum theoretical output at 100% capacity:
# 744 * 51,840 = ~38.5 million biscuits per machine for the entire month!
print("Maximum theoretical output at 100% (744h * 51,840/h):", 744 * 51840)

# If someone did SUM(TotalBiscuitsMade) for Biscuit Filling Machine:
print("SUM(TotalBiscuitsMade) for Biscuit Filling Machine:", r_df[r_df['Machine'] == 'Biscuit Filling Machine']['TotalBiscuitsMade'].sum())
# 1.3 BILLION biscuits! That's 34 times the theoretical maximum of the machine running 24/7 at 100% speed!
# Therefore SUM(TotalBiscuitsMade) CANNOT be the biscuits made!

# What about incremental increases (odometer diffs)?
bf = r_df[r_df['Machine'] == 'Biscuit Filling Machine'].copy()
bf['start'] = pd.to_datetime(bf['StartDateTime'], format='%d/%m/%y %H:%M')
bf = bf.sort_values('start').reset_index(drop=True)

# Calculate positive deltas when counter resets or increases
diffs = bf['TotalBiscuitsMade'].diff()
# Where diff < 0 (reset), the production from 0 to current is bf['TotalBiscuitsMade']
positive_prod = np.where(diffs > 0, diffs, 0)
print("Sum of positive diffs in TotalBiscuitsMade:", positive_prod.sum())

# What about GoodMadeBiscuits?
print("\nGoodMadeBiscuits stats for Biscuit Filling Machine:")
print("  Sum of GoodMadeBiscuits:", bf['GoodMadeBiscuits'].sum())
print("  Max of GoodMadeBiscuits:", bf['GoodMadeBiscuits'].max())
g_diffs = bf['GoodMadeBiscuits'].diff()
positive_good = np.where(g_diffs > 0, g_diffs, 0)
print("  Sum of positive diffs in GoodMadeBiscuits:", positive_good.sum())

# What about other machines?
print("\nOther machines GoodMadeBiscuits sums:")
for m, g in r_df.groupby('Machine'):
    print(f"  {m:28} | Sum Good: {g['GoodMadeBiscuits'].sum():10,d} | Sum Total: {g['TotalBiscuitsMade'].sum():10,d}")
