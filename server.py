import os
import re
import json
import time
import threading
import duckdb
import pandas as pd
import numpy as np
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI(title="Grandma EDNA's Biscuits - Industrial Analytics & SMED Digital Twin")

# Lock for DuckDB thread-safety
db_lock = threading.Lock()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

# Initialize DuckDB in-memory database
duck_conn = duckdb.connect(database=":memory:")

def load_tables():
    fact_path = os.path.join(PROCESSED_DIR, "fact_events_clean.csv")
    kpi_path = os.path.join(PROCESSED_DIR, "kpi_baseline_machines.csv")
    loss_path = os.path.join(PROCESSED_DIR, "loss_tree_summary.csv")
    products_path = os.path.join(DATA_DIR, "Products.csv")
    speed_path = os.path.join(DATA_DIR, "Target Speed.csv")
    machines_path = os.path.join(DATA_DIR, "Machine.csv")
    smed_path = os.path.join(PROCESSED_DIR, "smed_simulation_scenarios.csv")

    with db_lock:
        if os.path.exists(fact_path):
            df_fact = pd.read_csv(fact_path)
            duck_conn.execute("CREATE OR REPLACE TABLE fact_events AS SELECT * FROM df_fact")
        
        if os.path.exists(kpi_path):
            df_kpi = pd.read_csv(kpi_path)
            df_kpi.columns = [c.strip().replace('%', 'pct').replace(' ', '_') for c in df_kpi.columns]
            if 'Scheduled_Hours' in df_kpi.columns:
                df_kpi['Planned_Hours'] = df_kpi['Scheduled_Hours']
            duck_conn.execute("CREATE OR REPLACE TABLE kpi_machines AS SELECT * FROM df_kpi")
            
        if os.path.exists(loss_path):
            df_loss = pd.read_csv(loss_path)
            duck_conn.execute("CREATE OR REPLACE TABLE loss_tree AS SELECT * FROM df_loss")
            
        if os.path.exists(products_path):
            df_prod = pd.read_csv(products_path, encoding='utf-8-sig', sep=None, engine='python')
            df_prod.columns = [c.strip().replace('﻿', '') for c in df_prod.columns]
            duck_conn.execute("CREATE OR REPLACE TABLE products AS SELECT * FROM df_prod")

        if os.path.exists(speed_path):
            df_speed = pd.read_csv(speed_path, encoding='utf-8-sig', sep=None, engine='python')
            df_speed.columns = [c.strip().replace('﻿', '') for c in df_speed.columns]
            duck_conn.execute("CREATE OR REPLACE TABLE target_speeds AS SELECT * FROM df_speed")

        if os.path.exists(machines_path):
            df_mach = pd.read_csv(machines_path, encoding='utf-8-sig', sep=None, engine='python')
            df_mach.columns = [c.strip().replace('﻿', '') for c in df_mach.columns]
            duck_conn.execute("CREATE OR REPLACE TABLE machines AS SELECT * FROM df_mach")

        if os.path.exists(smed_path):
            df_smed = pd.read_csv(smed_path)
            duck_conn.execute("CREATE OR REPLACE TABLE smed_scenarios AS SELECT * FROM df_smed")

load_tables()

# Machine line mapping & short naming for clean visual charts
SHORT_NAMES = {
    'Biscuit Filling Machine': 'Llenadora',
    'Biscuit Sprinkling Machine': 'Rociadora',
    'Biscuit Pressing Machine': 'Prensadora',
    'Biscuit Boxing Machine': 'Encajonadora',
    'Biscuit Mixing Machine': 'Mezcladora',
    'Packaging Heat Machine': 'Envolvedora',
    'Biscuit Jam Machine': 'Dosif. Jam',
    'Biscuit Forming Machine': 'Formadora',
    'Biscuit Topping Machine': 'Decoradora',
    'Biscuit Heating Machine': 'Horno Túnel'
}

LINE_MAPPING = {
    'Biscuit Mixing Machine': 'Línea 1 (Sandwich)',
    'Biscuit Forming Machine': 'Línea 1 (Sandwich)',
    'Biscuit Heating Machine': 'Línea 1 (Sandwich)',
    'Biscuit Filling Machine': 'Línea 1 (Sandwich)',
    'Biscuit Topping Machine': 'Línea 1 (Sandwich)',
    'Packaging Heat Machine': 'Línea 1 (Sandwich)',
    'Biscuit Boxing Machine': 'Línea 1 (Sandwich)',
    'Biscuit Pressing Machine': 'Línea 2 (Prensadas)',
    'Biscuit Sprinkling Machine': 'Línea 2 (Prensadas)',
    'Biscuit Jam Machine': 'Línea 2 (Prensadas)'
}

LINE1_MACHINES = [m for m, l in LINE_MAPPING.items() if 'Línea 1' in l]
LINE2_MACHINES = [m for m, l in LINE_MAPPING.items() if 'Línea 2' in l]

@app.get("/api/health")
def health_check():
    return {"status": "ok", "plant": "Grandma EDNA's Biscuits", "version": "2.0.0", "lines": 2, "machines": 10}

@app.get("/api/filters")
def get_filter_options():
    with db_lock:
        prods = duck_conn.execute("SELECT DISTINCT Product FROM fact_events WHERE Product IS NOT NULL ORDER BY Product").fetchall()
        categories = duck_conn.execute("SELECT DISTINCT \"OEE Category\" FROM fact_events WHERE \"OEE Category\" IS NOT NULL ORDER BY \"OEE Category\"").fetchall()
        machines = duck_conn.execute("SELECT DISTINCT Machine FROM fact_events WHERE Machine IS NOT NULL ORDER BY Machine").fetchall()
    
    return {
        "products": [p[0] for p in prods if p[0]],
        "categories": [c[0] for c in categories if c[0]],
        "machines": [m[0] for m in machines if m[0]],
        "lines": ["Todas las Líneas", "Línea 1 (Sandwich - 6 SKUs)", "Línea 2 (Prensadas - 12 SKUs)"]
    }

@app.get("/api/kpis")
def get_kpis(line: str = "all", product: str = "all", category: str = "all"):
    clauses = []
    if line == "line1":
        quoted = ", ".join([f"'{m}'" for m in LINE1_MACHINES])
        clauses.append(f"Machine IN ({quoted})")
    elif line == "line2":
        quoted = ", ".join([f"'{m}'" for m in LINE2_MACHINES])
        clauses.append(f"Machine IN ({quoted})")
    
    if product != "all":
        clauses.append(f"Product = '{product}'")
        
    if category != "all":
        clauses.append(f"\"OEE Category\" = '{category}'")

    where_sql = ("WHERE " + " AND ".join(clauses)) if clauses else ""

    with db_lock:
        query_kpi = f"""
            SELECT 
                COUNT(*) AS total_events,
                ROUND(SUM(Duration_July_Hours), 2) AS total_hours,
                ROUND(SUM(CAST(TotalBiscuitsMade AS DOUBLE)), 0) AS total_biscuits,
                ROUND(SUM(CAST(GoodMadeBiscuits AS DOUBLE)), 0) AS good_biscuits,
                ROUND(SUM(CASE WHEN \"OEE Category\" = 'CC (Changeover Cleaning)' THEN Duration_July_Hours ELSE 0 END), 2) AS cc_hours,
                ROUND(SUM(CASE WHEN \"OEE Category\" = 'NO (No Order)' THEN Duration_July_Hours ELSE 0 END), 2) AS no_hours,
                ROUND(SUM(CASE WHEN \"OEE Category\" = 'PM (Maintenance)' THEN Duration_July_Hours ELSE 0 END), 2) AS pm_hours,
                ROUND(SUM(CASE WHEN \"OEE Category\" = '0' THEN Duration_July_Hours ELSE 0 END), 2) AS cat0_hours
            FROM fact_events
            {where_sql}
        """
        row = duck_conn.execute(query_kpi).fetchone()
        
        # Baseline machines OEE
        kpi_q = "SELECT Machine, Availability_pct, Performance_pct, Quality_pct, OEE_pct FROM kpi_machines"
        df_k = duck_conn.execute(kpi_q).fetchdf()

    if line == "line1":
        df_k = df_k[df_k['Machine'].isin(LINE1_MACHINES)]
    elif line == "line2":
        df_k = df_k[df_k['Machine'].isin(LINE2_MACHINES)]

    mean_avail = round(df_k['Availability_pct'].mean(), 2) if not df_k.empty else 80.12
    mean_perf = round(df_k['Performance_pct'].mean(), 2) if not df_k.empty else 74.05
    mean_qual = round(df_k['Quality_pct'].mean(), 2) if not df_k.empty else 98.24
    mean_oee = round((mean_avail * mean_perf * mean_qual) / 10000.0, 2)

    # Bottleneck Llenadora specifically
    filler_row = df_k[df_k['Machine'] == 'Biscuit Filling Machine']
    filler_oee = float(filler_row['OEE_pct'].values[0]) if not filler_row.empty else 37.90
    filler_avail = float(filler_row['Availability_pct'].values[0]) if not filler_row.empty else 67.19

    total_biscuits = row[2] if row[2] else 0
    good_biscuits = row[3] if row[3] else 0
    scrap_rate = round(((total_biscuits - good_biscuits) / total_biscuits * 100.0), 2) if total_biscuits > 0 else 1.8

    return {
        "mean_oee": mean_oee,
        "mean_avail": mean_avail,
        "mean_perf": mean_perf,
        "mean_qual": mean_qual,
        "world_class_gap": round(85.0 - mean_oee, 2),
        "filler_oee": filler_oee,
        "filler_avail": filler_avail,
        "total_events": row[0] or 0,
        "total_hours": row[1] or 0,
        "total_biscuits": total_biscuits,
        "good_biscuits": good_biscuits,
        "scrap_rate_pct": scrap_rate,
        "cc_hours": row[4] or 0,
        "no_hours": row[5] or 0,
        "pm_hours": row[6] or 0,
        "cat0_hours": row[7] or 0
    }

@app.get("/api/machines-overview")
def get_machines_overview(line: str = "all"):
    with db_lock:
        df_kpi = duck_conn.execute("""
            SELECT 
                Machine, 
                Type, 
                Planned_Hours, 
                Operating_Hours, 
                Availability_pct, 
                Performance_pct, 
                Quality_pct, 
                OEE_pct
            FROM kpi_machines
            ORDER BY OEE_pct ASC
        """).fetchdf()

    if line == "line1":
        df_kpi = df_kpi[df_kpi['Machine'].isin(LINE1_MACHINES)]
    elif line == "line2":
        df_kpi = df_kpi[df_kpi['Machine'].isin(LINE2_MACHINES)]

    result = []
    for _, r in df_kpi.iterrows():
        m_name = r['Machine']
        line_name = LINE_MAPPING.get(m_name, "Línea 1")
        is_bottleneck = (m_name == 'Biscuit Filling Machine' or m_name == 'Biscuit Sprinkling Machine')
        result.append({
            "machine": m_name,
            "machine_short": SHORT_NAMES.get(m_name, m_name),
            "type": r['Type'],
            "line": line_name,
            "planned_hours": float(r['Planned_Hours']),
            "operating_hours": float(r['Operating_Hours']),
            "availability_pct": float(r['Availability_pct']),
            "performance_pct": float(r['Performance_pct']),
            "quality_pct": float(r['Quality_pct']),
            "oee_pct": float(r['OEE_pct']),
            "is_bottleneck": is_bottleneck,
            "status": "CRITICAL" if r['OEE_pct'] < 50 else ("WARNING" if r['OEE_pct'] < 70 else "OPTIMAL")
        })
    return result

@app.get("/api/loss-tree")
def get_loss_tree(line: str = "all"):
    with db_lock:
        where_line = ""
        if line == "line1":
            quoted = ", ".join([f"'{m}'" for m in LINE1_MACHINES])
            where_line = f"WHERE Machine IN ({quoted})"
        elif line == "line2":
            quoted = ", ".join([f"'{m}'" for m in LINE2_MACHINES])
            where_line = f"WHERE Machine IN ({quoted})"

        if line in ["line1", "line2"]:
            q_cat = f"""
                SELECT 
                    CASE 
                        WHEN "OEE Category" = 'CC (Changeover Cleaning)' THEN 'Cambios y Limpiezas (CC)'
                        WHEN "OEE Category" = 'NO (No Order)' THEN 'Falta de Pedido / Sin Demanda (NO)'
                        WHEN "OEE Category" = '0' THEN 'Parada Mayor / Avería No Codificada (Cat 0)'
                        WHEN "OEE Category" = 'PM (Maintenance)' THEN 'Mantenimiento Preventivo (PM)'
                        ELSE 'Otras Paradas'
                    END AS Loss_Subcategory,
                    COUNT(*) AS Eventos,
                    ROUND(SUM(Duration_July_Hours), 2) AS Horas
                FROM fact_events
                {where_line}
                GROUP BY 1
                ORDER BY Horas DESC
            """
            df_loss = duck_conn.execute(q_cat).fetchdf()
            tot_h = df_loss['Horas'].sum()
            df_loss['%_Tiempo_Total'] = (df_loss['Horas'] / tot_h * 100.0).round(2) if tot_h > 0 else 0
        else:
            df_loss = duck_conn.execute("SELECT * FROM loss_tree ORDER BY Horas DESC").fetchdf()

        # Breakdown of CC
        cc_filter = (' AND ' + where_line.replace('WHERE ', '')) if where_line else ''
        q_cc = f"""
            SELECT 
                CASE 
                    WHEN Duration_July_Hours <= 1.0 THEN 'Cambio Rutinario SMED (<=60 min)'
                    ELSE 'Avería Oculta en CC (>60 min)'
                END AS sub_type,
                ROUND(SUM(Duration_July_Hours), 2) AS total_h,
                COUNT(*) AS events
            FROM fact_events
            WHERE "OEE Category" = 'CC (Changeover Cleaning)' {cc_filter}
            GROUP BY 1
        """
        df_cc_split = duck_conn.execute(q_cc).fetchdf()

    return {
        "tree_categories": df_loss.to_dict(orient="records"),
        "cc_subcategories": df_cc_split.to_dict(orient="records")
    }

@app.get("/api/pareto-smed")
def get_pareto_smed():
    with db_lock:
        # Pareto of Routine CC <= 60 min
        q_routine = """
            SELECT 
                Machine,
                ROUND(SUM(Duration_July_Hours), 2) AS routine_hours,
                COUNT(*) AS event_count
            FROM fact_events
            WHERE \"OEE Category\" = 'CC (Changeover Cleaning)' AND Duration_July_Hours <= 1.0
            GROUP BY Machine
            ORDER BY routine_hours DESC
        """
        df_routine = duck_conn.execute(q_routine).fetchdf()
        
        # Pareto of Breakdowns > 60 min
        q_breakdowns = """
            SELECT 
                Machine,
                ROUND(SUM(Duration_July_Hours), 2) AS breakdown_hours,
                COUNT(*) AS event_count
            FROM fact_events
            WHERE \"OEE Category\" = 'CC (Changeover Cleaning)' AND Duration_July_Hours > 1.0
            GROUP BY Machine
            ORDER BY breakdown_hours DESC
        """
        df_break = duck_conn.execute(q_breakdowns).fetchdf()

    # Add short names
    df_routine['machine_short'] = df_routine['Machine'].map(SHORT_NAMES).fillna(df_routine['Machine'])
    df_break['machine_short'] = df_break['Machine'].map(SHORT_NAMES).fillna(df_break['Machine'])

    # Calculate cumulative percentages
    tot_r = df_routine['routine_hours'].sum()
    df_routine['cum_pct'] = (df_routine['routine_hours'].cumsum() / tot_r * 100.0).round(2) if tot_r > 0 else 0

    tot_b = df_break['breakdown_hours'].sum()
    df_break['cum_pct'] = (df_break['breakdown_hours'].cumsum() / tot_b * 100.0).round(2) if tot_b > 0 else 0

    return {
        "routine_smed": df_routine.to_dict(orient="records"),
        "hidden_breakdowns": df_break.to_dict(orient="records")
    }

@app.get("/api/bottleneck-speed")
def get_bottleneck_speed():
    with db_lock:
        q_speed = """
            SELECT 
                Product,
                COUNT(*) AS event_count,
                ROUND(AVG(Duration_July_Hours * 60), 2) AS avg_duration_min,
                ROUND(SUM(CAST(TotalBiscuitsMade AS DOUBLE)), 0) AS total_made,
                ROUND(SUM(CAST(TotalBiscuitsMade AS DOUBLE)) / NULLIF(SUM(Duration_July_Hours), 0), 0) AS avg_speed_u_h
            FROM fact_events
            WHERE Machine = 'Biscuit Filling Machine' AND \"OEE Category\" = 'NO (No Order)'
            GROUP BY Product
            ORDER BY total_made DESC
        """
        df_speed = duck_conn.execute(q_speed).fetchdf()

    # Design speed vs observed speed
    return {
        "design_speed": 51840,
        "observed_median_speed": 38506,
        "speed_gap_u_h": 13334,
        "speed_loss_pct": 25.7,
        "products_performance": df_speed.to_dict(orient="records")
    }

class SMEDSimRequest(BaseModel):
    reduction_pct: float = 40.0
    margin_per_case: float = 3.50
    startup_scrap_pct: float = 1.5
    speed_u_h: float = 38506.0
    ot_shifts_saved: int = 26
    capex_audited: float = 23800.0

@app.post("/api/simulate-smed")
def simulate_smed(params: SMEDSimRequest):
    base_routine_hours = 123.52 # Base routine CC hours for Filling Machine
    
    hours_saved_month = round(base_routine_hours * (params.reduction_pct / 100.0), 2)
    hours_saved_year = round(hours_saved_month * 12.0, 2)
    
    gross_biscuits_month = round(hours_saved_month * params.speed_u_h, 0)
    gross_biscuits_year = round(gross_biscuits_month * 12.0, 0)
    
    quality_factor = 1.0 - (params.startup_scrap_pct / 100.0)
    net_biscuits_month = round(gross_biscuits_month * quality_factor, 0)
    net_biscuits_year = round(gross_biscuits_year * quality_factor, 0)
    
    cases_year = round(net_biscuits_year / 144.0, 0) # 144 biscuits per case (24 packs x 6)
    pallets_year = round(cases_year / 48.0, 0) # 48 cases per pallet
    pallets_month = round(pallets_year / 12.0, 0)
    
    gross_margin_year = round(cases_year * params.margin_per_case, 2)
    ot_savings_year = round(params.ot_shifts_saved * (6 * 8 * 28), 2) # 6 ops x 8 hrs x $28/hr
    total_benefit_year = round(gross_margin_year + ot_savings_year, 2)
    
    # Payback
    payback_days = round((params.capex_audited / total_benefit_year) * 365.0, 1) if total_benefit_year > 0 else 0
    roi_pct = round(((total_benefit_year - params.capex_audited) / params.capex_audited) * 100.0, 1) if params.capex_audited > 0 else 0
    
    # New projected OEE on Llenadora
    # Base planned hours: 566.9h. Base operating: 380.9h
    new_operating_hours = 380.92 + hours_saved_month
    new_avail = round((new_operating_hours / 566.9) * 100.0, 2)
    new_oee = round((new_avail * 0.5641 * 0.985), 2) # Performance 56.41%, Quality 98.5%
    delta_oee = round(new_oee - 37.90, 2)
    
    return {
        "hours_saved_month": hours_saved_month,
        "hours_saved_year": hours_saved_year,
        "gross_biscuits_month": gross_biscuits_month,
        "gross_biscuits_year": gross_biscuits_year,
        "net_biscuits_year": net_biscuits_year,
        "cases_year": cases_year,
        "pallets_year": pallets_year,
        "pallets_month": pallets_month,
        "gross_margin_year": gross_margin_year,
        "ot_savings_year": ot_savings_year,
        "total_benefit_year": total_benefit_year,
        "capex_audited": params.capex_audited,
        "payback_days": payback_days,
        "roi_pct": roi_pct,
        "new_availability_pct": new_avail,
        "new_oee_pct": new_oee,
        "delta_oee_pts": delta_oee
    }

@app.get("/api/pre-mortem-amfe")
def get_pre_mortem_amfe():
    failure_modes = [
        {
            "id": "MF-01",
            "name": "Inercia Térmica del Horno Túnel (Starvation)",
            "description": "El horno túnel de 60m tarda 35 min en estabilizar temperatura (-30°C); llenadora lista a los 15 min queda vacía esperando galletas frías.",
            "s_ini": 7, "o_ini": 8, "d_ini": 2, "npr_ini": 112,
            "countermeasure": "Programación Heijunka con menor delta T y preaviso a quemadores 20 min antes de fin de lote.",
            "s_fin": 4, "o_fin": 2, "d_fin": 2, "npr_fin": 16,
            "status": "CONTROLADO"
        },
        {
            "id": "MF-02",
            "name": "Bloqueo por Encartonadora (Downstream Choke)",
            "description": "Encartonadora registra paradas de cambio de hasta 276 min; buffer intermedio de 3 min colapsa y ahoga la llenadora.",
            "s_ini": 8, "o_ini": 7, "d_ini": 2, "npr_ini": 112,
            "countermeasure": "SMED simultáneo en encartonadora con galgas mecánicas de ajuste rápido y control dinámico de flujo.",
            "s_fin": 4, "o_fin": 2, "d_fin": 2, "npr_fin": 16,
            "status": "CONTROLADO"
        },
        {
            "id": "MF-03",
            "name": "Contaminación Cruzada por Alérgenos (Lácteos)",
            "description": "Arranque apresurado a los 15 min sin validación de QA; trazas de leche en lote no alérgeno fuerzan recall masivo.",
            "s_ini": 10, "o_ini": 5, "d_ini": 6, "npr_ini": 300,
            "countermeasure": "Protocolo ATP integrado al minuto 12 con luminómetro digital (<30 RLU); firma digital obligatoria en tablet.",
            "s_fin": 9, "o_fin": 1, "d_fin": 2, "npr_fin": 18,
            "status": "CONTROLADO"
        },
        {
            "id": "MF-04",
            "name": "Proliferación Bacteriana en Cabezal Gemelo",
            "description": "Cabezal lavado almacenado húmedo a 22°C incuba biopelícula bacteriana y Listeria monocytogenes.",
            "s_ini": 9, "o_ini": 6, "d_ini": 7, "npr_ini": 378,
            "countermeasure": "Secado con aire filtrado HEPA 0.01um, desinfección alcohólica al 70% y bolsa sellada con vencimiento 24h.",
            "s_fin": 8, "o_fin": 1, "d_fin": 2, "npr_fin": 16,
            "status": "CONTROLADO"
        },
        {
            "id": "MF-05",
            "name": "Sinéresis y Choque Térmico de Crema",
            "description": "Crema a 28°C sin agitación se separa; boquillas frías provocan cristalización alfa de grasa y taponamiento.",
            "s_ini": 6, "o_ini": 8, "d_ini": 3, "npr_ini": 144,
            "countermeasure": "Tanque móvil encamisado a 30°C con raspador continuo a 15 RPM y manta térmica en carro 5S.",
            "s_fin": 3, "o_fin": 2, "d_fin": 2, "npr_fin": 12,
            "status": "CONTROLADO"
        },
        {
            "id": "MF-06",
            "name": "Lesión Lumbar por Carga de Cabezal (NIOSH)",
            "description": "Operador levanta solo un bloque de acero de 32 kg superando el límite seguro NIOSH (Lifting Index 2.85).",
            "s_ini": 8, "o_ini": 6, "d_ini": 2, "npr_ini": 96,
            "countermeasure": "Montaje obligatorio a 4 manos asistido por brazo articulado neumático de gravedad cero ($LI < 1.0$).",
            "s_fin": 2, "o_fin": 1, "d_fin": 1, "npr_fin": 2,
            "status": "CONTROLADO"
        },
        {
            "id": "MF-07",
            "name": "Saturación de Almacén de Producto Terminado",
            "description": "271 pallets/mes adicionales saturan bodega y generan costo logístico 3PL si ventas no absorbe el volumen.",
            "s_ini": 6, "o_ini": 7, "d_ini": 3, "npr_ini": 126,
            "countermeasure": "Alineación quincenal S&OP (Sales & Operations Planning), lotes nivelados y contratos de distribución ágiles.",
            "s_fin": 4, "o_fin": 2, "d_fin": 2, "npr_fin": 16,
            "status": "CONTROLADO"
        }
    ]

    budget_breakdown = [
        {"item": "Cabezal Gemelo de Boquillas CNC AISI 316L", "initial": 2200, "audited": 9500, "justification": "Mecanizado monobloque con 12 pistones rotativos de precisión sanitaria micrométrica."},
        {"item": "Tanque Pulmón Encamisado con Agitador de Raspado", "initial": 0, "audited": 5200, "justification": "Camisa eléctrica a 30°C y motor reductor antiexplosión de 15 RPM para evitar sinéresis."},
        {"item": "Brazo Pescante Neumático de Gravedad Cero", "initial": 0, "audited": 3800, "justification": "Polipasto balanceado para elevación ergonómica segura de 32 kg (norma NIOSH)."},
        {"item": "Carro Móvil 5S Sanitario con Manta Calefactora", "initial": 1800, "audited": 2100, "justification": "Acero inoxidable con atemperador de utillaje para evitar choque frío en boquillas."},
        {"item": "Galgas Poka-Yoke y Abrazaderas Tri-Clamp 3A", "initial": 800, "audited": 1200, "justification": "Galgas rectificadas calibradas y abrazaderas de acople rápido grado alimentario."},
        {"item": "Kit Luminómetro Digital ATP y Swabs UltraSnap", "initial": 0, "audited": 2000, "justification": "Equipo Hygiena EnSURE Touch para validación microbiológica digital al minuto 12."}
    ]

    tot_ini = sum(b['initial'] for b in budget_breakdown)
    tot_aud = sum(b['audited'] for b in budget_breakdown)

    return {
        "failure_modes": failure_modes,
        "budget_breakdown": budget_breakdown,
        "total_initial_capex": tot_ini,
        "total_audited_capex": tot_aud,
        "delta_capex": tot_aud - tot_ini,
        "payback_audited_days": 14.9,
        "annual_benefit_usd": 581609.0
    }

class SqlRequest(BaseModel):
    query: str

# Tablas cargadas en memoria por este servidor — única superficie de datos
# que la consola SQL pública debe poder tocar.
SQL_ALLOWED_TABLES = (
    "fact_events", "kpi_machines", "loss_tree", "products",
    "target_speeds", "machines", "smed_scenarios",
)

# Palabras reservadas de SQL que no son nombres de tabla/columna reales y por
# tanto no disparan el chequeo de whitelist (evita falsos positivos en "select",
# "from", "where", "and", "or", "as", "on", "group", "by", "order", etc.).
SQL_KEYWORDS_SKIP = {
    "select", "with", "from", "where", "and", "or", "not", "in", "as",
    "on", "join", "left", "right", "inner", "outer", "group", "by",
    "order", "limit", "offset", "asc", "desc", "having", "distinct",
    "case", "when", "then", "else", "end", "is", "null", "between",
    "like", "union", "all", "cross", "using", "count", "sum", "avg",
    "min", "max", "over", "partition", "cast", "true", "false",
}

SQL_TIMEOUT_SECONDS = 5
SQL_ROW_LIMIT = 100

def validate_readonly_sql(raw_query: str) -> str:
    clean_q = raw_query.strip().rstrip(";")
    if not clean_q:
        raise ValueError("La consulta está vacía.")
    if ";" in clean_q:
        raise ValueError("Solo se permite una única sentencia SQL por consulta.")
    lowered = clean_q.lower()
    if not (lowered.startswith("select") or lowered.startswith("with")):
        raise ValueError("Solo se permiten consultas de lectura (SELECT / WITH).")

    # Alias de CTE (WITH alias AS (...), alias2 AS (...)) cuentan como tablas
    # válidas dentro de esta misma consulta.
    cte_aliases = set(re.findall(r"(?:with|,)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+as\s*\(", lowered))
    allowed = set(SQL_ALLOWED_TABLES) | cte_aliases

    # Whitelist: toda referencia a FROM/JOIN debe apuntar a una de las tablas
    # cargadas en memoria (o a un alias de CTE definido arriba). Esto bloquea
    # funciones de lectura de archivo de DuckDB (read_csv_auto, read_text,
    # glob, rutas de archivo, pragma_*...) que un blocklist de keywords no cubre.
    table_refs = re.findall(r"\b(?:from|join)\s+([a-zA-Z_][a-zA-Z0-9_\.\"]*)", lowered)
    if not table_refs:
        raise ValueError("La consulta debe incluir al menos un FROM sobre una tabla permitida.")
    for ref in table_refs:
        table_name = ref.strip('"').split(".")[-1]
        if table_name not in allowed:
            raise ValueError(
                f"Tabla no permitida: '{table_name}'. Tablas disponibles: {', '.join(SQL_ALLOWED_TABLES)}."
            )

    # Cualquier otro identificador "tipo función" (palabra seguida de "(")
    # que no sea una función SQL agregada/estándar queda bloqueado, para
    # evitar llamadas a funciones de tabla o de sistema de DuckDB.
    func_calls = set(re.findall(r"\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", lowered))
    suspicious_funcs = func_calls - SQL_KEYWORDS_SKIP - {
        "round", "abs", "coalesce", "lower", "upper", "trim", "date_trunc",
        "extract", "strftime", "concat", "length", "substr", "row_number",
        "rank", "dense_rank", "ifnull", "nullif",
    }
    if suspicious_funcs:
        raise ValueError(f"Función no permitida en consola de solo lectura: {', '.join(sorted(suspicious_funcs))}")

    if "limit" not in lowered:
        clean_q = f"{clean_q}\nLIMIT {SQL_ROW_LIMIT}"
    return clean_q

def _run_with_timeout(conn, sql: str, timeout_s: float) -> pd.DataFrame:
    """Ejecuta sql en un hilo aparte y cancela la consulta vía conn.interrupt()
    si excede timeout_s (DuckDB no soporta un statement_timeout nativo)."""
    result = {}

    def _worker():
        try:
            result["df"] = conn.execute(sql).fetchdf()
        except Exception as e:
            result["error"] = e

    t = threading.Thread(target=_worker, daemon=True)
    t.start()
    t.join(timeout_s)
    if t.is_alive():
        conn.interrupt()
        t.join(timeout_s)
        raise TimeoutError(f"La consulta excedió el límite de {timeout_s}s y fue cancelada.")
    if "error" in result:
        raise result["error"]
    return result["df"]

@app.post("/api/sql")
def execute_sql(req: SqlRequest):
    t0 = time.time()
    try:
        clean_q = validate_readonly_sql(req.query)
        with db_lock:
            res_df = _run_with_timeout(duck_conn, clean_q, SQL_TIMEOUT_SECONDS)
        ms = round((time.time() - t0) * 1000, 2)
        total_rows = len(res_df)
        res_limited = res_df.head(100).copy()
        for col in res_limited.columns:
            if pd.api.types.is_datetime64_any_dtype(res_limited[col]):
                res_limited[col] = res_limited[col].astype(str)
        res_limited = res_limited.fillna("")
        return {
            "success": True,
            "columns": list(res_limited.columns),
            "rows": res_limited.to_dict(orient="records"),
            "total_rows": total_rows,
            "execution_ms": ms
        }
    except Exception as e:
        ms = round((time.time() - t0) * 1000, 2)
        return {
            "success": False,
            "error": str(e),
            "execution_ms": ms
        }

@app.get("/", response_class=HTMLResponse)
def serve_index():
    template_path = os.path.join(BASE_DIR, "templates", "index.html")
    if os.path.exists(template_path):
        with open(template_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Dashboard: templates/index.html not found.</h1>", status_code=404)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8502))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True)
