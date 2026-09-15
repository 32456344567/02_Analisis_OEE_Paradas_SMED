import pandas as pd

df = pd.read_csv('data/Total Report.csv', sep=';', decimal=',')
for col in df.select_dtypes(include='object').columns:
    df[col] = df[col].str.strip()

print("=== INSPECTING GOODMADEBISCUITS DURING 'NO' IN OTHER MACHINES ===")
for m in sorted(df['Machine'].unique()):
    sub = df[df['Machine'] == m]
    no_sub = sub[sub['OEE Category'] == 'NO (No Order)']
    cc_sub = sub[sub['OEE Category'] == 'CC (Changeover Cleaning)']
    
    print(f"\n{m}:")
    print(f"  NO rows: {len(no_sub)} | Dur: {no_sub['Duration'].sum()/60:.1f}h | Total sum: {no_sub['TotalBiscuitsMade'].sum():,} | Good sum: {no_sub['GoodMadeBiscuits'].sum():,}")
    print(f"  CC rows: {len(cc_sub)} | Dur: {cc_sub['Duration'].sum()/60:.1f}h | Total sum: {cc_sub['TotalBiscuitsMade'].sum():,} | Good sum: {cc_sub['GoodMadeBiscuits'].sum():,}")
