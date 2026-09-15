import pandas as pd

df = pd.read_csv('data/Total Report.csv', sep=';', decimal=',')
for col in df.select_dtypes(include='object').columns:
    df[col] = df[col].str.strip()

pack = df[df['Machine'] == 'Packaging Heat Machine'].head(10)
print("=== PACKAGING HEAT MACHINE FIRST 10 ROWS ===")
for i, r in pack.iterrows():
    print(f"{r['StartDateTime']} to {r['EndDateTime']} | dur:{r['Duration']:6.2f}m | total:{r['TotalBiscuitsMade']:4} | good:{r['GoodMadeBiscuits']:4} | cat:{r['OEE Category']} | prod:{r['Product']}")
