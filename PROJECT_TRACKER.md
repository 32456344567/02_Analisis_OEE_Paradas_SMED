# 📋 PROJECT TRACKER: Optimización OEE, Paradas Crónicas y Reducción SMED

Este documento es el tablero de control de avance del proyecto. Registra el estado de cada componente, entregable y archivo para asegurar que toda la cadena (Local -> GitHub -> Railway -> Notion) se cumpla con excelencia técnica y metodológica.

---

## 📌 Estado General del Proyecto
* **Proyecto:** 02_Analisis_OEE_Paradas_SMED
* **Fase Actual:** Fase 1 - Configuración Inicial y Auditoría de Datos
* **Estado:** 🟡 En Progreso
* **Enfoque de Visualización:** Dashboard Web Interactivo en Python (FastAPI / Streamlit) desplegado en Railway (Capex Cero, sin gemelo digital)

---

## 🗺️ Mapa de Entregables y Checklist Pieza por Pieza

### 🧪 Nivel 1: Ingeniería de Datos, Auditoría y Cálculo OEE (Python)
- [x] **Configuración del entorno de trabajo:**
  - [x] Creación de carpetas base (`notebooks/`, `src/`, `app/`, `docs/`, `entregables_planta/`).
  - [x] Archivo de requerimientos de desarrollo (`requirements.txt`).
- [x] **Notebook 01 (`notebooks/01_etl_modelado_oee.ipynb`):**
  - [x] Auditoría de integridad de las 4 fuentes (`Total Report.csv`, `Target Speed.csv`, `Products.csv`, `Machine.csv`).
  - [x] Normalización de campos temporales (`StartDateTime`, `EndDateTime`, `Duration`).
  - [x] Validación de solapamientos temporales y balance de horas de planta (julio 2021).
  - [x] **Guía Maestra para Entrevistas Laborales (De principio a fin):** [`EXPLICACION_PASO_A_PASO_PROYECTO.md`](EXPLICACION_PASO_A_PASO_PROYECTO.md).
  - [x] **Auditoría Forense de Telemetría IoT y Resolución de la Paradoja `NO`:** [`docs/AUDITORIA_FASE_1_OEE_DIAGNOSTICO.md`](docs/AUDITORIA_FASE_1_OEE_DIAGNOSTICO.md).
  - [x] Formulación matemática rigurosa de Disponibilidad ($A$), Rendimiento ($P$) y Calidad ($Q$).
  - [x] Cálculo del OEE basal corregido de la fábrica (**58.21% OEE Medio**, Cuello de botella Llenadora en **37.90%**) frente a Clase Mundial (85%).
  - [x] Tabla consolidada de OEE y componentes por máquina (`data/processed/kpi_baseline_machines.csv`).
- [x] **Notebook 02 (`notebooks/02_loss_tree_pareto_smed.ipynb`):**
  - [x] **Auditoría Forense de Paradas y Mantenimiento:** [`docs/AUDITORIA_FASE_2_MANTENIMIENTO_Y_PARADAS.md`](docs/AUDITORIA_FASE_2_MANTENIMIENTO_Y_PARADAS.md).
  - [x] **Auditoría Integral 360° de la Fase 2 (Las 5 Fallas Ocultas):** [`docs/AUDITORIA_INTEGRAL_FASE_2_TODAS_LAS_FALLAS.md`](docs/AUDITORIA_INTEGRAL_FASE_2_TODAS_LAS_FALLAS.md).
  - [x] Descubrimiento de las **2 Líneas de Producción Independientes** (Línea 1 Sandwich vs. Línea 2 Prensadas/Decoradas).
  - [x] Descubrimiento de **350.1 h de Averías Mecánicas Ocultas** dentro de `CC` (>60 min) y **132.5 h de Parada Mayor** (Categoría `0`).
  - [x] Cuantificación de las **166.0 h de pérdidas de Rendimiento/Velocidad** en el Árbol de Pérdidas de la Llenadora.
  - [x] Diagrama de Pareto 80/20 de SMED Real: La Llenadora concentra el **58.49% de los cambios rutinarios** de toda la fábrica (123.5 h, 1,957 eventos).
  - [x] Diagrama de Pareto 80/20 de Averías Mecánicas Ocultas: Encajonadora (83.8 h), Formadora (64.5 h) y Horno (62.6 h) concentran las mayores fallas.
  - [x] Diagnóstico de Cuello de Botella y Causas Físicas: Velocidad real observada (~38,506 u/h) vs. velocidad de diseño (51,840 u/h).
  - [x] Simulación SMED Realista (Track A - Capex Cero): Reducción del 40% sobre los cambios rutinarios de la Llenadora recupera **49.4 h/mes** y genera **+22.8 millones de galletas/año** (validada capacidad aguas abajo en Encajonadora).
  - [x] Definición del Roadmap Dual: Track A (Lean SMED) + Track B (TPM Mantenimiento Autónomo y Predictivo).
  - [x] Exportación de datasets analíticos en `data/processed/` (`loss_tree_summary.csv`, `pareto_machines_smed_routine.csv`, `pareto_machines_breakdowns.csv`, `pareto_products_cc.csv`, `speed_analysis_bottleneck.csv`, `smed_simulation_scenarios.csv`).

---

### 🏭 Nivel 2: Lean Manufacturing & Toolkit Operativo de Planta (Fase 3)
- [x] **Auditoría Forense Pre-Mortem de Fase 3 (Modos de Falla en Planta):**
  - [x] Documento técnico exhaustivo: [`docs/AUDITORIA_INTEGRAL_FASE_3_PREMORTEM_Y_FALLAS_SMED.md`](docs/AUDITORIA_INTEGRAL_FASE_3_PREMORTEM_Y_FALLAS_SMED.md).
  - [x] Análisis de 7 modos de falla críticos: Desacople e inercia térmica del Horno Túnel, Bloqueo de Encartonadora (276 min de CC), Protocolo sanitario ATP/Alérgenos (BRCGS/IFS), Reología y sinéresis de cremas, Ergonomía y ecuación de levantamiento NIOSH (32 kg), Secuenciación Heijunka y saturación de almacén (3,253 pallets).
  - [x] Matriz AMFE (FMEA) cuantitativa con Severidad, Ocurrencia, Detección y reducción de NPR de riesgo alto a riesgo controlado.
- [x] **Matriz SMED de Reducción de Tiempos de Cambio (Versión 3.0 Auditada):**
  - [x] Archivo Excel interactivo enriquecido con 4 hojas: [`entregables_planta/Matriz_SMED_Reduccion_Setups.xlsx`](entregables_planta/Matriz_SMED_Reduccion_Setups.xlsx) (incorporada hoja `Auditoria_AMFE_Riesgos` con presupuesto auditado y matriz FMEA).
  - [x] Guía técnica de ingeniería: [`entregables_planta/Matriz_SMED_Reduccion_Setups.md`](entregables_planta/Matriz_SMED_Reduccion_Setups.md).
  - [x] Mapeo paso a paso de las 11 actividades en el cuello de botella (`Biscuit Filling Machine`).
  - [x] Cronograma Hombre-Máquina balanceado con validación microbiológica QA en paralelo (minuto 10-12).
  - [x] Plan de optimización y dispositivos técnicos blindados: Carro móvil 5S con manta calefactora, brazo pescante neumático de gravedad cero, conexiones Tri-Clamp 1/4 de vuelta, conjunto de cabezal gemelo prelavado con secado HEPA y galgas mecánicas de color.
  - [x] Reducción demostrada: **de 45 min a 15 min (-66.7%) en cambios mayores** y **de 123.5 h a 74.1 h (-40.0%) en paradas rutinarias mensuales**.
- [x] **Cuantificación Financiera del Caso de Negocio (Capex Cero / Defendible):**
  - [x] Documento ejecutivo: [`entregables_planta/Caso_Negocio_Financiero_Capex_Cero.md`](entregables_planta/Caso_Negocio_Financiero_Capex_Cero.md).
  - [x] 49.4 h netas recuperadas al mes (**592.9 h al año**).
  - [x] Generación de **+22.48 millones de galletas vendibles netas al año** (+156,174 cajas comerciales).
  - [x] Beneficio bruto proyectado: **+$546,609 USD / año** + **$35,000 USD** en horas extras eliminadas = **+$581,609 USD/año**.
  - [x] Inversión requerida auditada: **$23,800 USD** (Capex menor robusto con brazo ergonómico, tanque encamisado y kit ATP) con **Payback de 14.9 días**.
  - [x] Ahorro vs compra de máquina nueva: **$226,200 USD de Capex evitado**.
  - [x] Plan logístico de absorción en bodega (S&OP para 271 pallets/mes).
- [x] **Reporte A3 de Excelencia Operacional:**
  - [x] Documento oficial Toyota: [`entregables_planta/Reporte_A3_Excelencia_Operacional.md`](entregables_planta/Reporte_A3_Excelencia_Operacional.md).
  - [x] Estructura A3 completa: Antecedentes, Condición Actual, Objetivos SMART auditados, Diagrama de Ishikawa 6M, 5 Porqués, Roadmap Dual (Track A SMED + Track B TPM), Cronograma Gantt de 8 semanas con activos auditados y Estandarización SOP.

---

### 🌐 Nivel 3: Dashboard Web Interactivo de Operaciones (Python + Railway)
- [x] **Arquitectura de la Aplicación Web (`server.py` y `templates/index.html`):**
  - [x] Motor analítico ultra rápido con **FastAPI + DuckDB in-memory** con bloqueo de concurrencia thread-safe.
  - [x] Diseño estético de alta gama basado en el **Proyecto 1**: Barra lateral SCADA Navy (`#0A1120`), acentos azules (`#2563EB`), tarjetas elevadas (`card-elevated`) sobre fondo `#F8FAFC`, tipografía *Inter* y *JetBrains Mono*.
  - [x] **5 Módulos Interactivos con ApexCharts reactivos:**
    - [x] **Módulo 1: Visión Ejecutiva OEE Global:** Tacómetros radiales OEE/A/P/Q, comparación vs Clase Mundial (85%), cascada de horas perdidas de planta.
    - [x] **Módulo 2: Arquitectura & Cuello de Botella:** Visualizador de las dos líneas desacopladas (7 + 3 activos), matriz OEE interactiva de 10 activos, gráfico de dispersión de velocidad observada (38,506 u/h) vs diseño (51,840 u/h).
    - [x] **Módulo 3: Árbol de Pérdidas y Pareto 80/20:** Diagramas de Pareto interactivos para cambios rutinarios ($\le 60\text{ min}$) y averías mecánicas crónicas (>60 min).
    - [x] **Módulo 4: Simulador Interactivo SMED (What-If):** Sliders dinámicos (% reducción, margen $/caja, merma arranque) con cálculo reactivo instantáneo de horas, galletas, cajas, pallets, EBITDA y Payback.
    - [x] **Módulo 5: Auditoría Forense Pre-Mortem & AMFE:** Matriz de riesgos FMEA cuantitativa con NPR inicial vs final, desglose de cotizaciones sanitarias reales ($23,800 USD) y cronograma Hombre-Máquina balanceado.
- [x] **Preparación para Despliegue en Railway:**
  - [x] `Procfile` configurado (`web: uvicorn server:app --host 0.0.0.0 --port $PORT`).
  - [x] `requirements.txt` ligero y compatible con Python 3.10-3.13.
  - [x] Endpoint de monitoreo `/api/health` listo para verificaciones de disponibilidad en la nube.

---

### 💼 Nivel 4: Portafolio Profesional, GitHub y Notion
- [ ] **Repositorio GitHub:**
  - [ ] `README.md` principal estructurado con capturas del dashboard, arquitectura y justificación técnica.
  - [ ] Configuración de `.gitignore` (exclusión de temporales y caches).
- [ ] **Ficha Técnica para Notion (`docs/CASO_DE_ESTUDIO_NOTION.md`):**
  - [ ] Redacción ejecutiva con metodología STAR (Situación, Tarea, Acción, Resultado).
  - [ ] Tabla de impacto cuantificado (Incremento proyectado de OEE %, Horas anuales liberadas, Ahorro sin Capex).
  - [ ] Enlaces directos a la demo en vivo en Railway y al repositorio.
- [ ] **Guía de Publicación (`docs/GUIA_SUBIDA_GITHUB_RAILWAY.md`):**
  - [ ] Instrucciones paso a paso para desplegar en Railway en 3 minutos.
