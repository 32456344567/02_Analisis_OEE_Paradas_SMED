import pandas as pd
import numpy as np

df = pd.read_csv('data/Total Report.csv', sep=';', decimal=',')
for c in df.select_dtypes(include='object').columns:
    df[c] = df[c].str.strip()

print("=================================================================")
print("=== AUDITORÍA FORENSE DE FASE 2: MANTENIMIENTO Y PARADAS ===")
print("=================================================================")

print("\n--- 1. LAS 6 FILAS DE CATEGORÍA PM (Mantenimiento Preventivo) ---")
pm_df = df[df['OEE Category'] == 'PM (Maintenance)']
for i, r in pm_df.iterrows():
    m = r['Machine']
    s = r['StartDateTime']
    e = r['EndDateTime']
    d = r['Duration']
    sku = r['Product']
    print(f"Fila {i:4} | {m:26} | {s} a {e} | Dur: {d:6.2f} min ({d/60:4.2f} h) | {sku}")

print(f"\nTotal horas PM registradas: {pm_df['Duration'].sum()/60:.2f} h")

print("\n--- 2. LAS 12 FILAS DE CATEGORÍA '0' (Paradas no clasificadas) ---")
zero_df = df[df['OEE Category'] == '0']
for i, r in zero_df.iterrows():
    m = r['Machine']
    s = r['StartDateTime']
    e = r['EndDateTime']
    d = r['Duration']
    sku = r['Product']
    print(f"Fila {i:4} | {m:26} | {s} a {e} | Dur: {d:7.2f} min ({d/60:5.2f} h) | {sku}")

print(f"\nTotal horas Categoría 0: {zero_df['Duration'].sum()/60:.2f} h")

print("\n--- 3. EVENTOS ANÓMALOS DISFRAZADOS DENTRO DE 'CC (Changeover Cleaning)' ---")
cc_df = df[df['OEE Category'] == 'CC (Changeover Cleaning)'].copy()
long_cc = cc_df[cc_df['Duration'] > 60].sort_values('Duration', ascending=False)
print(f"Total eventos CC que duraron MÁS DE 1 HORA: {len(long_cc)} eventos!")
print(f"Horas acumuladas en estos eventos > 1h: {long_cc['Duration'].sum()/60:.2f} horas!")

print("\nTop 15 eventos más largos etiquetados como 'CC':")
for i, r in long_cc.head(15).iterrows():
    m = r['Machine']
    s = r['StartDateTime']
    e = r['EndDateTime']
    d = r['Duration']
    sku = r['Product']
    print(f"Fila {i:4} | {m:26} | {s} a {e} | Dur: {d:7.2f} min ({d/60:5.2f} h) | {sku}")
