import pandas as pd

m_df = pd.read_csv('data/Machine.csv', sep=';')
p_df = pd.read_csv('data/Products.csv', sep=';')
t_df = pd.read_csv('data/Target Speed.csv', sep=';')
r_df = pd.read_csv('data/Total Report.csv', sep=';', decimal=',')

# Clean whitespaces
for df in [m_df, p_df, t_df, r_df]:
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].str.strip()

print("=== MACHINE.CSV ===")
print(m_df)
print("\n=== PRODUCTS.CSV ===")
print(p_df)
print("\n=== TARGET SPEED.CSV ===")
print(t_df.head(10))
print("Target speed unique machines:", t_df['Machine'].nunique())
print("Target speed counts per machine:\n", t_df['Machine'].value_counts())

print("\nTarget speed values per machine:")
for m, g in t_df.groupby('Machine'):
    print(f"  {m:28} | Speeds: {g['TARGET_Biscuits_per_hour'].unique().tolist()} | Products count: {g['Product'].nunique()}")
