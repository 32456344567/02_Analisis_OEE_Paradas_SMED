# Optimización de OEE y Reducción de Tiempos de Cambio (SMED)
**Caso: Grandma EDNA's Biscuits — Línea de Galletería Continua**
**Autor:** Ing. Angelo Apolo | Optimización de Procesos Industriales & Datos

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.13-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![DuckDB](https://img.shields.io/badge/DuckDB-In--Memory%20SQL-FFF000?style=flat&logo=duckdb&logoColor=black)](https://duckdb.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-High%20Performance-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Metodología](https://img.shields.io/badge/Metodología-Lean%20SMED%20%7C%20TOC-blue?style=flat)](#metodología)
[![Licencia](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## En una frase

A partir de 8,044 registros de telemetría de una planta de galletas, identifiqué la máquina que limita toda la producción (cuello de botella), cuanticé cuánta capacidad se pierde por cambios de formato lentos, y diseñé un plan Lean SMED que recupera esa capacidad **sin comprar maquinaria nueva**.

## 1. El problema

La planta necesitaba más capacidad de producción. La respuesta típica de gerencia ante esto es comprar una máquina adicional ($250,000 USD, 9 meses de espera). Antes de aprobar ese gasto, analicé los datos operativos de julio 2021 para responder: **¿la planta realmente necesita más máquinas, o está desperdiciando la capacidad que ya tiene?**

## 2. El diagnóstico (OEE)

Usando el estándar internacional OEE (Disponibilidad × Rendimiento × Calidad, norma ANSI/ISA-95) sobre los eventos de máquina de julio 2021 (744 horas de planta):

| Métrica | Valor | Referencia Clase Mundial |
|---|---|---|
| OEE Global de Planta | **58.21%** | 85.0% |
| Disponibilidad | 80.12% | ≥90% |
| Rendimiento | 74.05% | ≥95% |
| Calidad | 98.24% | ≥99.9% |

La fábrica opera en realidad como **dos líneas independientes** (Sandwich y Prensadas). En la línea principal (70% de la facturación), la **Llenadora de Crema (`Biscuit Filling Machine`)** es el cuello de botella: su OEE es de solo **37.90%**, muy por debajo del resto de la planta.

**Causa raíz:** la Llenadora acumula **123.5 horas al mes** en cambios de formato y limpieza rutinarios (1,957 eventos, 58.5% de sus paradas totales). Cada cambio toma en promedio 45 minutos.

> Nota técnica: el dataset original traía dos trampas de datos — un sensor que reportaba lecturas acumuladas tipo odómetro (no producción por evento) y una categoría `NO (No Order)` mal etiquetada que en realidad correspondía a turnos de producción normal. Corregir esto fue lo que llevó el OEE calculado de un valor inicial absurdo (10.96%) al valor real y verificable de 58.21%. Detalle completo en [`docs/AUDITORIA_FASE_1_OEE_DIAGNOSTICO.md`](docs/AUDITORIA_FASE_1_OEE_DIAGNOSTICO.md).

## 3. La solución (Lean SMED)

Apliqué la metodología SMED (Single-Minute Exchange of Die) al cambio de formato de la Llenadora:

1. **Preparación externa:** cremas, utillajes y recetas se preparan mientras la línea sigue produciendo el lote anterior.
2. **Cabezal de recambio rápido:** acoples sanitarios de cuarto de vuelta en vez de desmontaje con herramientas.
3. **Validación de calidad en paralelo:** el control de higiene se ejecuta durante el cambio, no después.

**Resultado proyectado:** tiempo de cambio de **45 min → 15 min (-66.7%)**, recuperando el 40% de las 123.5 h/mes perdidas → **49.4 horas de producción liberadas cada mes**.

Plan de acción detallado, tarea por tarea, en [`entregables_planta/Matriz_SMED_Reduccion_Setups.xlsx`](entregables_planta/Matriz_SMED_Reduccion_Setups.xlsx).

## 4. El caso de negocio

| | Comprar máquina nueva | Plan Lean SMED |
|---|---|---|
| Inversión | $250,000 USD | **$23,800 USD** |
| Tiempo de implementación | 6–9 meses | **8 semanas** |
| Beneficio anual | ~$581,000 USD | **$581,609 USD** |
| Payback | 5.2 meses | **14.9 días** |

Las 49.4 h/mes recuperadas equivalen a **+22.48 millones de galletas vendibles al año** (+156,174 cajas comerciales), a la velocidad real observada de la línea (38,506 unidades/hora). Memoria de cálculo completa en [`entregables_planta/Caso_Negocio_Financiero_Capex_Cero.md`](entregables_planta/Caso_Negocio_Financiero_Capex_Cero.md).

## 5. Dashboard interactivo

* **Backend:** Python + FastAPI + DuckDB in-memory para consultas analíticas sobre los datos crudos.
* **Frontend:** Tailwind CSS + ApexCharts.
* **4 vistas:** Diagnóstico OEE de planta, Cuello de botella y Pareto de paradas, Simulador financiero SMED (What-If), Consola SQL.

### Ejecutar localmente

```bash
git clone https://github.com/32456344567/02_Analisis_OEE_Paradas_SMED.git
cd 02_Analisis_OEE_Paradas_SMED
pip install -r requirements.txt
python server.py
```

Abrir en el navegador: **http://localhost:8502**

## 6. Estructura del repositorio

```text
02_Analisis_OEE_Paradas_SMED/
├── server.py                    # FastAPI + DuckDB + endpoints analíticos
├── templates/index.html         # Dashboard
├── notebooks/                   # ETL, cálculo de OEE, Pareto de paradas
├── data/                        # Datos crudos y procesados
├── entregables_planta/          # Matriz SMED (Excel) y caso de negocio financiero
├── docs/                        # Auditoría técnica de datos (OEE y paradas)
├── anexos_avanzados/            # Análisis adicionales (FMEA, ergonomía, guía extendida) — material de referencia, no parte del caso principal
└── requirements.txt
```

## Autor

**Ing. Angelo Apolo**
Ingeniero Químico · Optimización de Procesos Industriales, Analítica de Datos & Lean Manufacturing
Guayaquil, Ecuador · [LinkedIn](https://www.linkedin.com/in/angelo-a-44a9a323b) · [Portafolio Web](https://32456344567.github.io/)
