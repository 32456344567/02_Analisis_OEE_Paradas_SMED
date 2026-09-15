# Optimización de OEE de Planta, Cuello de Botella & Reducción de Tiempos de Cambio (SMED)
**Caso Industrial Real: Grandma EDNA's Biscuits — Línea Continua de Galletería**  
**Autor:** Ing. Angelo Apolo | Especialista en Optimización de Procesos Industriales & Datos  

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.13-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![DuckDB](https://img.shields.io/badge/DuckDB-In--Memory%20SQL-FFF000?style=flat&logo=duckdb&logoColor=black)](https://duckdb.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-High%20Performance-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Metodología](https://img.shields.io/badge/Metodología-Lean%20SMED%20%7C%20TOC-blue?style=flat)](#metodología-industrial)
[![Licencia](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📌 1. Resumen Ejecutivo (El Reto de Negocio)

En manufactura continua, la decisión estándar de una gerencia ante la falta de capacidad suele ser aprobar presupuestos de capital elevados (Capex) para comprar maquinaria adicional. Este proyecto demuestra la alternativa más rentable: **recuperar capacidad instalada oculta mediante analítica de datos, Teoría de Restricciones (TOC) y Lean SMED con una fracción mínima de inversión**.

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│ IMPACTO FINANCIERO & OPERATIVO AUDITADO (CAPEX CERO / RETORNO DEFENDIBLE)                   │
├──────────────────────────┬──────────────────────────┬───────────────────────────────────────┤
│ +$581,391 USD / año      │ +49.4 h / mes            │ 14.9 Días de Payback                  │
│ Beneficio Bruto Adicional│ Capacidad Recuperada     │ Inversión $23.8k vs Máquina de $250k  │
├──────────────────────────┼──────────────────────────┼───────────────────────────────────────┤
│ +22.48 M Galletas / año  │ -66.7% Tiempo de Cambio  │ +156,174 Cajas Comerciales / año      │
│ Producción Vendible Neta │ De 45 min a 15 min (SMED)│ Absorbibles por S&OP en Bodega        │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔍 2. Diagnóstico Técnico & Descomposición OEE

A partir de **8,044 eventos de telemetría de máquina** correspondientes al mes base (julio 2021, 744 horas de planta), se modeló matemáticamente el OEE canónico de acuerdo con la norma internacional **ANSI/ISA-95**:

$$\text{OEE} = \text{Disponibilidad } (A) \times \text{Rendimiento } (P) \times \text{Calidad } (Q)$$

### Resultados Basales de Planta:
* **OEE Global Medio:** **58.21%** (frente al estándar de **85.0% Clase Mundial** &rarr; Brecha de **-26.79 puntos porcentuales**).
* **Disponibilidad ($A$):** **80.12%** &rarr; 147.9 horas de paradas no programadas en el mes.
* **Rendimiento ($P$):** **74.05%** &rarr; Velocidad real observada de 38,506 u/h vs. estándar de diseño de 51,840 u/h (-25.7% de pérdida por marcha lenta).
* **Calidad ($Q$):** **98.24%** &rarr; 458.3 millones de unidades vendibles (1.76% de scrap en empaque).

---

## ⚙️ 3. Identificación de la Restricción (Teoría de Restricciones - TOC)

El análisis estratificado reveló que la fábrica opera **dos líneas desacopladas**:
1. **Línea 1 (Galletas Sandwich - 70% de la facturación):** Cadena de 7 equipos (*Mezcladora &rarr; Formadora &rarr; Horno Túnel &rarr; Llenadora &rarr; Decoradora &rarr; Envolvedora &rarr; Encajonadora*).
2. **Línea 2 (Galletas Prensadas - 30% de la facturación):** Cadena de 3 equipos (*Prensadora &rarr; Rociadora &rarr; Dosificadora de Jam*).

> **Hallazgo Crítico:** La **Llenadora de Galletas (`Biscuit Filling Machine`)** es el cuello de botella físico de toda la planta:
> * **OEE de la Llenadora:** **37.90%** (el más bajo de la fábrica).
> * **Causa Raíz:** Acumula **123.5 horas de parada al mes en Cambios de Formato y Limpieza (`CC`)** (1,957 eventos, representando el **58.49% de sus paradas totales**).

---

## 🛠️ 4. Plan de Acción Lean SMED (De 45 min a 15 min)

Para eliminar las 123.5 horas de parada sin comprometer la inocuidad alimentaria ni la calidad, se aplicó la metodología **SMED (Single-Minute Exchange of Die)**:

1. **Desacople de Tareas Externas (5S):** Preparación de cremas, utillajes y recetas mientras la línea sigue produciendo el lote anterior (**-12 min**).
2. **Cabezal Gemelo Sanitario Prelavado & Poka-Yoke:** Sustitución del cabezal monobloque con acoples rápidos Tri-Clamp de 1/4 de vuelta y galgas fijas calibradas sin necesidad de llaves inglesas (**-10 min**).
3. **Validación Microbiológica ATP en Paralelo:** Test rápido con hisopo digital al minuto 12 en lugar de esperar la inspección tradicional (**-8 min**).
4. **Resultado Operativo:** Reducción del tiempo de cambio de **45 min a 15 min (-66.7%)**, liberando **+49.4 horas mensuales de producción neta**.

---

## 💰 5. Caso de Negocio: Lean SMED vs. Compra de Maquinaria Nueva

| Parámetro | Alternativa Tradicional (Capex Mayor) | Propuesta Lean SMED (Angelo Apolo) |
| :--- | :--- | :--- |
| **Solución** | Compra de 1 Llenadora adicional de reserva | Estandarización SMED + Cabezal Gemelo |
| **Inversión Requerida** | **$250,000 USD** | **$23,800 USD** (Cabezal CNC, tanque encamisado, kit ATP) |
| **Tiempo de Implementación**| 6 a 9 meses (importación y montaje) | **8 semanas** (Gantt estructurado) |
| **Beneficio Anual** | +$581,000 USD / año | **+$581,391 USD / año** |
| **Período de Recuperación** | 5.2 Meses | **14.9 Días** |
| **Capex Ahorrado** | $0 USD | **$226,200 USD de capital protegido** |

---

## 💻 6. Dashboard Web & Arquitectura de Software

El proyecto incluye un dashboard web interactivo diseñado con la misma sobriedad y elegancia que caracteriza a herramientas industriales de clase mundial:

* **Backend:** **Python + FastAPI** con **DuckDB In-Memory** para procesamiento columnar analítico de alta velocidad (tiempo de respuesta de queries: **< 3 ms**).
* **Frontend:** **Tailwind CSS + ApexCharts + Vanilla JS** sin dependencias pesadas de Node/npm.
* **4 Vistas Principales:**
  1. **Diagnóstico & OEE Planta:** Cascada de pérdidas (Waterfall) y donut de paradas.
  2. **Cuello de Botella & Paradas:** Arquitectura de 2 líneas, ranking horizontal de activos y Pareto 80/20.
  3. **Plan SMED & Simulación Financiera:** Simulador What-If reactivo con presets de 1-clic y comparativa de inversión.
  4. **Consola SQL DuckDB:** Editor y ejecutor de consultas SQL nativas sobre los datos en memoria.

---

## 🚀 7. Ejecución Local en 2 Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/32456344567/02_Analisis_OEE_Paradas_SMED.git
cd 02_Analisis_OEE_Paradas_SMED

# 2. Instalar dependencias y arrancar el servidor
pip install -r requirements.txt
python server.py
```

Abre en tu navegador: **[http://localhost:8081](http://localhost:8081)**

---

## 📂 8. Estructura de Entregables

```text
02_Analisis_OEE_Paradas_SMED/
├── server.py                                  # Servidor FastAPI + DuckDB in-memory + endpoints analíticos
├── templates/
│   └── index.html                             # Dashboard web ejecutivo reactivo
├── data/
│   ├── Total Report.csv                       # Telemetría de 8,044 eventos operativos
│   ├── Target Speed.csv                       # Estándares nominales de velocidad
│   ├── Products.csv                           # Catálogo de 18 SKUs
│   ├── Machine.csv                            # Catálogo de 10 activos de planta
│   └── processed/                             # Datasets procesados y consolidados
├── entregables_planta/
│   ├── Matriz_SMED_Reduccion_Setups.xlsx      # Matriz SMED interactiva en Excel (4 hojas con AMFE)
│   ├── Caso_Negocio_Financiero_Capex_Cero.md  # Justificación financiera para Directorio
│   └── Reporte_A3_Excelencia_Operacional.md   # Reporte A3 oficial metodología Toyota
├── docs/
│   ├── AUDITORIA_FASE_1_OEE_DIAGNOSTICO.md    # Auditoría forense de datos y paradoja NO
│   ├── AUDITORIA_INTEGRAL_FASE_2_TODAS_LAS_FALLAS.md # Descubrimiento de las 2 líneas y averías ocultas
│   └── AUDITORIA_INTEGRAL_FASE_3_PREMORTEM_Y_FALLAS_SMED.md # Matriz FMEA de riesgos operativos
└── requirements.txt                           # Dependencias ligeras de producción
```

---

## 👤 Autor

**Ing. Angelo Apolo**  
*Ingeniero Químico · Especialista en Optimización de Procesos Industriales, Analítica de Datos & Lean Manufacturing*  
* Guayaquil, Ecuador  
* [LinkedIn](https://www.linkedin.com/in/angelo-a-44a9a323b) · [Portafolio Web](https://32456344567.github.io/)
