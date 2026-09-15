import pandas as pd

df = pd.read_csv('data/Total Report.csv', sep=';', decimal=',')
for col in df.select_dtypes(include='object').columns:
    df[col] = df[col].str.strip()
df['start'] = pd.to_datetime(df['StartDateTime'], format='%d/%m/%y %H:%M')
df['end'] = pd.to_datetime(df['EndDateTime'], format='%d/%m/%y %H:%M')

print("=== TIMELINE AND DURATIONS PER MACHINE ===")
for m, g in df.groupby('Machine'):
    s_min = g['start'].min()
    e_max = g['end'].max()
    dur_h = g['Duration'].sum() / 60
    rows = len(g)
    print(f"{m:28} | Rows: {rows:4} | Min: {s_min} | Max: {e_max} | Dur: {dur_h:7.1f}h")
