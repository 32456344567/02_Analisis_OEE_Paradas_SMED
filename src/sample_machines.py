import pandas as pd

r_df = pd.read_csv('data/Total Report.csv', sep=';', decimal=',')
for col in r_df.select_dtypes(include='object').columns:
    r_df[col] = r_df[col].str.strip()

for m in sorted(r_df['Machine'].unique()):
    sub = r_df[r_df['Machine'] == m]
    print(f"\n==================== {m} ({len(sub)} rows) ====================")
    print("OEE Categories:", sub['OEE Category'].value_counts().to_dict())
    print("TotalBiscuitsMade range:", sub['TotalBiscuitsMade'].min(), "-", sub['TotalBiscuitsMade'].max())
    print("GoodMadeBiscuits range:", sub['GoodMadeBiscuits'].min(), "-", sub['GoodMadeBiscuits'].max())
    print("Duration (min) sum:", sub['Duration'].sum(), "mean:", sub['Duration'].mean())
    print("Sample 3 rows:")
    print(sub[['StartDateTime', 'EndDateTime', 'Duration', 'TotalBiscuitsMade', 'GoodMadeBiscuits', 'OEE Category', 'Product']].head(3))
