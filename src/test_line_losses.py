import duckdb
import pandas as pd

conn = duckdb.connect(':memory:')
df = pd.read_csv('data/processed/fact_events_clean.csv')
conn.execute('CREATE TABLE fact_events AS SELECT * FROM df')

print("All Categories:")
for r in conn.execute('SELECT "OEE Category", round(sum(Duration_July_Hours), 1) as h, count(*) FROM fact_events GROUP BY 1 ORDER BY h DESC').fetchall():
    print(" ", r)

print("\nLine 1 Categories:")
for r in conn.execute("SELECT \"OEE Category\", round(sum(Duration_July_Hours), 1) as h, count(*) FROM fact_events WHERE Machine IN ('Biscuit Mixing Machine', 'Biscuit Forming Machine', 'Biscuit Heating Machine', 'Biscuit Filling Machine', 'Biscuit Topping Machine', 'Packaging Heat Machine', 'Biscuit Boxing Machine') GROUP BY 1 ORDER BY h DESC").fetchall():
    print(" ", r)

print("\nLine 2 Categories:")
for r in conn.execute("SELECT \"OEE Category\", round(sum(Duration_July_Hours), 1) as h, count(*) FROM fact_events WHERE Machine IN ('Biscuit Pressing Machine', 'Biscuit Sprinkling Machine', 'Biscuit Jam Machine') GROUP BY 1 ORDER BY h DESC").fetchall():
    print(" ", r)
