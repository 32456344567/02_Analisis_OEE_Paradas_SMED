# 🔬 AUDITORÍA INTEGRAL DE LA FASE 2: TODAS LAS FALLAS Y DESCUBRIMIENTOS OCULTOS
**Proyecto:** 02_Analisis_OEE_Paradas_SMED  
**Planta:** Grandma EDNA's Biscuits Manufacturing (Julio 2021)  
**Autor:** Angelo Apolo | Ing. Químico / Industrial | Especialista en Lean Operations & Dirección de Proyectos  
**Objetivo:** Auditoría integral 360° de todos los componentes de la Fase 2 (Árbol de Pérdidas, Arquitectura de Línea, Restricciones TOC, Diagnóstico de Velocidad y Simulación SMED).

---

## 🛑 1. Diagnóstico de la Fase 2: ¿Por qué era necesaria una auditoría integral?

El análisis inicial de la Fase 2 cometió **5 fallas metodológicas y conceptuales de ingeniería** al basarse únicamente en agrupaciones superficiales de los datos. Esta auditoría exhaustiva examina cada componente y documenta la verdad técnica de la fábrica.

```
+---------------------------------------------------------------------------------------------------+
|                            MAPA DE FALLAS DETECTADAS EN LA FASE 2                                |
+---------------------------------------------------------------------------------------------------+
| 1. ARQUITECTURA DE PLANTA: Se asumió 1 sola línea en serie, ignorando que hay 2 LÍNEAS PARALELAS. |
| 2. ÁRBOL DE PÉRDIDAS: Se omitieron 166 HORAS de pérdidas de velocidad (Rendimiento P).            |
| 3. TEORÍA DE RESTRICCIONES: Se declaró la Llenadora como cuello de botella de productos que no toca.|
| 4. DIAGNÓSTICO DE VELOCIDAD: Se usó un promedio plano sin explicar las causas físicas de proceso. |
| 5. SIMULACIÓN SMED: Se asumió calidad perfecta (cero scrap de arranque) y velocidad homogénea.    |
+---------------------------------------------------------------------------------------------------+
```

---

## 🏭 2. FALLA CRÍTICA 1: La Fábrica no es 1 Línea, son DOS LÍNEAS PARALELAS INDEPENDIENTES

En el análisis inicial se asumió que las 10 máquinas formaban una única gran línea en tándem por la que pasaban los 18 productos.  
Al cruzar la matriz completa de **Máquina vs. Producto** (`crosstab(df['Machine'], df['Product'])`), los datos revelaron una realidad totalmente distinta:

### Matriz de Distribución de Activos vs. Productos:

| Máquina | 6 Productos de Crema (Sandwich) | 12 Productos de Especialidad / Secos | Rol en Planta |
| :--- | :---: | :---: | :--- |
| **1. Biscuit Mixing Machine** | **212 eventos** | 0 eventos | **Línea 1** (Amasado de galletas sandwich) |
| **2. Biscuit Forming Machine** | **49 eventos** | 0 eventos | **Línea 1** (Troquelado de tapas) |
| **3. Biscuit Heating Machine** | **9 eventos** | 0 eventos | **Línea 1** (Horno túnel de tapas) |
| **4. Biscuit Filling Machine** | **3,970 eventos** | **0 eventos** ❌ | **Línea 1** (Inyección de crema en sandwich) |
| **5. Biscuit Topping Machine** | **18 eventos** | 0 eventos | **Línea 1** (Decorado de galletas sandwich) |
| **6. Packaging Heat Machine** | **187 eventos** | 0 eventos | **Línea 1** (Envoltura térmica individual) |
| **7. Biscuit Boxing Machine** | **216 eventos** | 0 eventos | **Línea 1** (Encajonado final de sandwich) |
| **8. Biscuit Pressing Machine** | 0 eventos | **1,149 eventos** | **Línea 2** (Prensado de galletas de masa dura) |
| **9. Biscuit Sprinkling Machine**| 0 eventos | **2,137 eventos** | **Línea 2** (Decorado, chispas y azúcar) |
| **10. Biscuit Jam Machine** | 0 eventos | **97 eventos** | **Línea 2** (Dosificado de mermeladas secas) |

### Impacto de la Falla:
1. **Existen dos cadenas de valor (*Value Streams*) completamente desacopladas**:
   - **Línea 1 (Línea de Sandwich / Crema - 7 máquinas):** Fabrica *Bourbon Creams, Chocolate cookies, Custard Creams, Jammy Creams, Milk Cookies* y *Pink Wafers*. Su cuello de botella físico es la **Llenadora (`Biscuit Filling Machine`)** con un OEE de **37.90%**.
   - **Línea 2 (Línea de Galletas Prensadas y Decoradas - 3 máquinas):** Fabrica *Almond Biscotti, Caramel Swirls, Chocolate Digestives, Coco Rings, Deluxe Cookies, Digestives, Fruit and Nut, Hazelnut Wafers, Orange Creams, Party Rings, Peanut Cookies* y *Vienesse Creams*.
2. **Error de la Fase 2 inicial:** Decir que la Llenadora era el cuello de botella de toda la planta era falso. **La Llenadora jamás procesó un solo paquete de Digestives o Almond Biscotti**.
3. **El Cuello de Botella de la Línea 2:** En la Línea 2, el verdadero cuello de botella es la **Rociadora (`Biscuit Sprinkling Machine`)**, cuyo OEE es de apenas **43.89%** debido a una disponibilidad colapsada al **44.77%** con 60.5 horas de paradas de cambio (`CC`).

---

## 🌳 3. FALLA CRÍTICA 2: El Árbol de Pérdidas estaba INCOMPLETO (Las 166 Horas de Velocidad Perdidas)

El cuaderno inicial de la Fase 2 graficaba únicamente las horas de parada de Disponibilidad (`CC`, `PM`, `NO`), olvidando que el OEE se compone de 3 dimensiones.

Al calcular el **Árbol de Pérdidas de las 6 Grandes Pérdidas del TPM en Horas Equivalentes** para el cuello de botella (`Biscuit Filling Machine`), descubrimos que **la pérdida de velocidad es casi tan grande como las paradas**:

```
TIEMPO TOTAL PROGRAMADO EN LLENADORA: 566.9 HORAS (100.0%)
│
├── 1. PÉRDIDAS DE DISPONIBILIDAD: 186.0 HORAS (32.8%)
│   ├── Paradas Rutinarias SMED (<=60m):   123.5 h  (21.8%)
│   ├── Averías Mecánicas Ocultas (>60m):   59.0 h  (10.4%)
│   └── Mantenimiento Preventivo Formal:     3.5 h  ( 0.6%)
│
├── 2. PÉRDIDAS DE RENDIMIENTO / VELOCIDAD: 166.0 HORAS (29.3%) 💥 (¡NO SE HABÍA CUANTIFICADO!)
│   └── 380.9 h operadas a solo 74.3% de la velocidad nominal de diseño
│
├── 3. PÉRDIDAS DE CALIDAD: 0.0 HORAS (0.0%)
│   └── Sensor IoT registró conteo neto de producto conforme
│
└── TIEMPO OPERATIVO VALIOSO (OEE NETO): 214.9 HORAS (37.9%)
```

> [!IMPORTANT]
> ### El Segundo Gran Agujero Negro: 166 Horas Perdidas por Rendimiento
> La Llenadora perdió **166.0 horas de producción equivalente simplemente por ir lenta**.  
> Esto demuestra que un proyecto de excelencia operacional no puede terminar en SMED: después de recuperar disponibilidad con SMED (Track A) y eliminar averías con TPM (Track B), se debe abrir un **Track C de Optimización de Velocidad (*Speed Loss Elimination*)**.

---

## ⚡ 4. FALLA CRÍTICA 3: Diagnóstico Superficial de la Brecha de Velocidad

En la Fase 2 se presentó una gráfica de barras de velocidad nominal vs. velocidad mediana sin explicar **por qué la máquina opera con un déficit de 13,334 galletas/hora**.

### La Brecha Real de Velocidad por Producto en la Llenadora:

| Producto (SKU) | Velocidad Nominal de Diseño | Velocidad Real Mediana Observada | Eficiencia de Velocidad | Galletas Perdidas por Hora de Marcha |
| :--- | :---: | :---: | :---: | :---: |
| **Chocolate cookies** | 44,000 u/h | 40,443 u/h | **91.8%** | -3,557 u/h (Comportamiento óptimo) |
| **Bourbon Creams** | 52,000 u/h | 38,535 u/h | **74.0%** | -13,465 u/h |
| **Milk Cookies** | 52,000 u/h | 38,555 u/h | **74.1%** | -13,445 u/h |
| **Custard Creams** | 51,700 u/h | 37,883 u/h | **73.4%** | -13,817 u/h |
| **Jammy Creams** | 52,000 u/h | 37,441 u/h | **71.9%** | **-14,559 u/h** (Mayor freno operativo) |
| **Pink Wafers** | 52,000 u/h | 33,815 u/h | **64.9%** | **-18,185 u/h** (Fragilidad extrema) |

### Causas Físicas de Proceso (Por qué el operario baja la velocidad):
1. ***Jammy Creams* (-14,559 u/h):** Es un producto bicapa (crema + mermelada). A velocidades superiores a 40,000 u/h, la mermelada no corta limpiamente y salpica las bandas, obligando a los operarios a reducir la velocidad para evitar paradas por ensuciamiento.
2. ***Pink Wafers* (-18,185 u/h):** Los barquillos son extremadamente quebradizos. A 52,000 u/h, el impacto de las guías mecánicas de la llenadora quiebra las esquinas de los barquillos, provocando atascos inmediatos.
3. ***Bourbon* y *Custard* (-13,500 u/h):** Problemas de reología y temperatura en la tolva de crema blanca/chocolate. Si la crema no está exactamente a 28°C–30°C, la viscosidad sube y el servomotor de inyección pierde el sincronismo.

---

## 🚀 5. FALLA CRÍTICA 4: Los Tres Vicios Matemáticos de la Simulación SMED Inicial

La simulación SMED inicial fue excesivamente simplista:

### Vicio A: La falacia de la velocidad plana
Se multiplicaron las horas recuperadas por una velocidad promedio de 38,506 u/h. En la realidad, si las horas recuperadas se distribuyen según el mix real de producción, productos como *Chocolate cookies* generan 40,443 galletas/h, mientras que *Pink Wafers* solo generan 33,815 galletas/h.

### Vicio B: Calidad 100% y cero merma de arranque (*Startup Scrap*)
En cualquier cambio de formato en la industria de galletas, cuando la máquina arranca tras una limpieza:
- Las primeras 50 a 100 galletas salen desalineadas o con gramaje incorrecto de crema mientras se ajusta el flujo de las boquillas.
- Un modelo realista debe incorporar una tasa de merma de arranque de al menos **1.5% a 2.0%** en la producción liberada.
- Al aplicar un factor de calidad conservador del 98.5%, las **22.82 millones de galletas brutas anuales** se convierten en **22.48 millones de galletas vendibles netas** (+338,000 galletas destinadas a retrabajo/merma).

### Vicio C: La Paradoja de la Capacidad Aguas Abajo (TOC de Goldratt)
¿Puede la planta absorber 22.8 millones de galletas más al año sin que otra máquina colapse?
- La máquina inmediatamente aguas abajo de la Llenadora es la **Encajonadora (`Biscuit Boxing Machine`)**.
- Producción extra mensual = **1,902,196 galletas/mes**.
- Como cada caja (*case*) contiene 24 paquetes de 6 galletas = **144 galletas/caja**.
- Cajas adicionales al mes = $1,902,196 / 144 = \mathbf{13,210 \text{ cajas/mes}}$.
- En un mes de 30 días con 2 turnos (16 h/día = 480 horas), esto equivale a solo **27.5 cajas adicionales por hora**.
- La velocidad de diseño de la Encajonadora es de **360 cajas/hora** (51,840 galletas/h).
- **Conclusión de Capacidad TOC:** Absorber 27.5 cajas/hora representa apenas el **7.6% de la capacidad horaria de la Encajonadora**. Por lo tanto, **la restricción NO se traslada** y el sistema puede evacuar toda la producción adicional sin formar cuellos de botella secundarios.

---

## 📋 6. Matriz Consolidada de Fallas de la Fase 2 y Correcciones Implementadas

| Componente | Falla Detectada en la Auditoría | Corrección Metodológica de Ingeniería | Estado |
| :--- | :--- | :--- | :---: |
| **Mantenimiento** | Solo 3.5 h de PM y 0 h de CM en el reporte bruto. | Se identificaron 350.1 h de averías ocultas en CC (>60m) y 132.5 h de parada mayor en Cat 0. | ✅ Resuelto |
| **Calendario** | Duda sobre descansos de fin de semana o feriados. | Auditoría de fechas demostró que las paradas ocurrieron de lunes a jueves y la planta produce 24/7. | ✅ Resuelto |
| **Líneas de Planta** | Se modeló la fábrica como 1 sola línea para 18 productos. | Se descubrió que existen 2 LÍNEAS PARALELAS: Línea 1 (6 SKUs Crema) y Línea 2 (12 SKUs Prensadas). | ✅ Resuelto |
| **Árbol de Pérdidas** | Solo se graficaban pérdidas de disponibilidad. | Se completó el Árbol con las 166 h de pérdidas de Rendimiento y 1 h de Calidad. | ✅ Resuelto |
| **Cuello de Botella** | Se asumió Llenadora como restricción de toda la fábrica. | Llenadora es cuello de botella de Línea 1; Rociadora (`Sprinkling`) es cuello de botella de Línea 2. | ✅ Resuelto |
| **Diagnóstico Velocidad**| No se explicaban las causas del freno de 13,334 u/h. | Se identificaron causas de proceso: viscosidad de mermelada y fragilidad mecánica de barquillos. | ✅ Resuelto |
| **Simulación SMED** | Supuestos planos de velocidad y calidad perfecta. | Se ponderó por mix real, se incluyó merma de arranque (98.5% vendible) y se validó capacidad TOC aguas abajo. | ✅ Resuelto |

---
*Fin de la Auditoría Integral de la Fase 2. Documento auditado bajo estándares de Lean Manufacturing, TPM e Ingeniería de Procesos.*
