import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import os

os.makedirs('entregables_planta', exist_ok=True)
wb = openpyxl.Workbook()

# Setup sheets
ws1 = wb.active
ws1.title = 'Matriz_SMED_Llenadora'
ws2 = wb.create_sheet(title='Resumen_Etapas_Shingo')
ws3 = wb.create_sheet(title='Impacto_Financiero_Planta')

# Paleta de colores industriales ejecutivos
header_fill = PatternFill(start_color='1F4E78', end_color='1F4E78', fill_type='solid') # Azul corporativo oscuro
sub_fill = PatternFill(start_color='D9E1F2', end_color='D9E1F2', fill_type='solid')    # Azul suave
ext_fill = PatternFill(start_color='E2EFDA', end_color='E2EFDA', fill_type='solid')    # Verde suave (Externa)
opt_fill = PatternFill(start_color='FFF2CC', end_color='FFF2CC', fill_type='solid')    # Amarillo suave (Optimizada)
total_fill = PatternFill(start_color='B4C6E7', end_color='B4C6E7', fill_type='solid')  # Azul medio

font_header = Font(name='Calibri', size=11, bold=True, color='FFFFFF')
font_bold = Font(name='Calibri', size=11, bold=True)
font_regular = Font(name='Calibri', size=10)
font_title = Font(name='Calibri', size=14, bold=True, color='1F4E78')
font_subtitle = Font(name='Calibri', size=10, italic=True, color='595959')

thin_border = Border(
    left=Side(style='thin', color='BFBFBF'),
    right=Side(style='thin', color='BFBFBF'),
    top=Side(style='thin', color='BFBFBF'),
    bottom=Side(style='thin', color='BFBFBF')
)

double_bottom_border = Border(
    left=Side(style='thin', color='BFBFBF'),
    right=Side(style='thin', color='BFBFBF'),
    top=Side(style='thin', color='BFBFBF'),
    bottom=Side(style='double', color='1F4E78')
)

# ==============================================================================
# HOJA 1: MATRIZ SMED DETALLADA DE LA LLENADORA
# ==============================================================================
ws1['A1'] = "MATRIZ TÉCNICA DE REDUCCIÓN DE TIEMPOS DE CAMBIO (SMED)"
ws1['A1'].font = font_title
ws1['A2'] = "Activo Crítico: Biscuit Filling Machine (Cuello de Botella - Línea 1) | Cambio de Receta: Custard Creams a Jammy Creams"
ws1['A2'].font = font_subtitle

headers1 = [
    'Paso #', 'Descripción Operativa de la Tarea', 'Responsable',
    'Clasificación Inicial (Antes)', 'Tiempo Antes (min)',
    'Estrategia de Optimización Lean / SMED', 'Clasificación Propuesta (Después)',
    'Tiempo Después (min)', 'Minutos Ahorrados', '% Reducción', 'Técnica de Ingeniería Aplicada'
]

for col_idx, h in enumerate(headers1, 1):
    cell = ws1.cell(row=4, column=col_idx, value=h)
    cell.fill = header_fill
    cell.font = font_header
    cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
ws1.row_dimensions[4].height = 28

tasks = [
    (1, 'Parada de máquina, corte de alimentación y aplicación LOTO', 'Operador 1', 'Interna', 3.0, 'Mantener como interna por seguridad. Check-list visual estandarizado.', 'Interna', 2.0, 'Estandarización 5S'),
    (2, 'Buscar herramientas manuales (llaves fijas y Allen) en taller mecánico', 'Operador 2', 'Interna', 5.0, 'Convertir en Externa. Carro móvil 5S con herramientas fijadas al pie de máquina antes de apagar.', 'Externa', 0.0, 'Conversión a Externa (OED)'),
    (3, 'Esperar por la nueva receta de crema y mermelada desde almacén', 'Operador 1', 'Interna', 6.0, 'Convertir en Externa. Tanque pulmón pre-posicionado y atemperado a 28°C 15 min antes de fin de lote.', 'Externa', 0.0, 'Conversión a Externa (OED)'),
    (4, 'Drenar y purgar residuos de crema del lote anterior en la tolva', 'Operador 1', 'Interna', 4.0, 'Mantener interna. Se instala válvula de purga rápida con manguera de desagüe directo.', 'Interna', 2.5, 'Simplificación Técnica'),
    (5, 'Desmontar boquillas dosificadoras y mangueras con llave fija', 'Operador 2', 'Interna', 6.0, 'Optimizar interna. Reemplazar pernos roscados por abrazaderas sanitarias Tri-Clamp de 1/4 vuelta.', 'Interna', 1.5, 'Sujeción Rápida Sin Llaves'),
    (6, 'Llevar boquillas sucias a zona de lavado y esperar lavado manual', 'Operador 2', 'Interna', 8.0, 'Convertir en Externa. Cabezal gemelo de reserva pre-lavado y pre-ensamblado listo al pie de máquina.', 'Externa', 0.0, 'Conjunto Gemelo Pre-lavado'),
    (7, 'Instalar nuevo juego de boquillas dosificadoras limpias', 'Operador 1', 'Interna', 5.0, 'Montaje rápido del cabezal gemelo limpio mediante guías deslizantes y clamp rápido.', 'Interna', 2.0, 'Acoplamiento Rápido'),
    (8, 'Conectar mangueras de alimentación de crema nueva', 'Operador 2', 'Interna', 3.0, 'Conexión rápida push-fit sin tornillos con empaque sanitario integrado.', 'Interna', 1.0, 'Conexión Push-fit'),
    (9, 'Carga de crema y cebado del sistema de inyección', 'Operador 1', 'Interna', 4.0, 'Carga por gravedad desde tanque pulmón pre-elevado; purga con pulsador rápido.', 'Interna', 2.0, 'Alimentación Automática'),
    (10, 'Ajuste y calibración manual de gramaje a prueba y error (pesaje)', 'Operador 2', 'Interna', 6.0, 'Topes micrométricos fijos con codificación de color por receta. Cero calibración a ciegas.', 'Interna', 2.0, 'Calibración Rígida (Galgas)'),
    (11, 'Despeje de línea, retiro de LOTO y arranque de lote', 'Operador 1', 'Interna', 2.0, 'Checklist de 3 puntos en panel HMI antes de dar marcha.', 'Interna', 2.0, 'Estandarización')
]

for row_idx, task in enumerate(tasks, 5):
    ws1.cell(row=row_idx, column=1, value=task[0])
    ws1.cell(row=row_idx, column=2, value=task[1])
    ws1.cell(row=row_idx, column=3, value=task[2])
    ws1.cell(row=row_idx, column=4, value=task[3])
    ws1.cell(row=row_idx, column=5, value=task[4])
    ws1.cell(row=row_idx, column=6, value=task[5])
    ws1.cell(row=row_idx, column=7, value=task[6])
    ws1.cell(row=row_idx, column=8, value=task[7])
    ws1.cell(row=row_idx, column=9, value=f"=E{row_idx}-H{row_idx}")
    ws1.cell(row=row_idx, column=10, value=f"=I{row_idx}/E{row_idx}")
    ws1.cell(row=row_idx, column=11, value=task[8])
    
    ws1.row_dimensions[row_idx].height = 22
    for c in range(1, 12):
        cell = ws1.cell(row=row_idx, column=c)
        cell.font = font_regular
        cell.border = thin_border
        if c in [1, 3, 4, 7]: cell.alignment = Alignment(horizontal='center', vertical='center')
        elif c in [5, 8, 9]: 
            cell.alignment = Alignment(horizontal='right', vertical='center')
            cell.number_format = '0.0'
        elif c == 10:
            cell.alignment = Alignment(horizontal='right', vertical='center')
            cell.number_format = '0.0%'
        else:
            cell.alignment = Alignment(horizontal='left', vertical='center')
            
        if task[6] == 'Externa':
            ws1.cell(row=row_idx, column=7).fill = ext_fill
            ws1.cell(row=row_idx, column=8).fill = ext_fill

# Totales Hoja 1
tot_row = 16
ws1.row_dimensions[tot_row].height = 24
ws1.cell(row=tot_row, column=2, value="TOTAL TIEMPO DE PARADA DE MÁQUINA (min)").font = font_bold
ws1.cell(row=tot_row, column=5, value="=SUM(E5:E15)").font = font_bold
ws1.cell(row=tot_row, column=8, value="=SUM(H5:H15)").font = font_bold
ws1.cell(row=tot_row, column=9, value=f"=E{tot_row}-H{tot_row}").font = font_bold
ws1.cell(row=tot_row, column=10, value=f"=I{tot_row}/E{tot_row}").font = font_bold

for c in range(1, 12):
    cell = ws1.cell(row=tot_row, column=c)
    cell.fill = total_fill
    cell.border = double_bottom_border
    if c in [5, 8, 9]: 
        cell.alignment = Alignment(horizontal='right', vertical='center')
        cell.number_format = '0.0'
    elif c == 10: 
        cell.alignment = Alignment(horizontal='right', vertical='center')
        cell.number_format = '0.0%'

col_widths1 = {1: 8, 2: 46, 3: 14, 4: 16, 5: 14, 6: 48, 7: 18, 8: 15, 9: 15, 10: 13, 11: 30}
for col_idx, width in col_widths1.items():
    ws1.column_dimensions[get_column_letter(col_idx)].width = width


# ==============================================================================
# HOJA 2: RESUMEN METODOLÓGICO POR ETAPAS DE SHIGEO SHINGO
# ==============================================================================
ws2['A1'] = "EVOLUCIÓN DEL TIEMPO DE CAMBIO SEGÚN LAS 4 ETAPAS DE SHIGEO SHINGO"
ws2['A1'].font = font_title
ws2['A2'] = "Metodología Lean SMED aplicada al Cuello de Botella (Biscuit Filling Machine)"
ws2['A2'].font = font_subtitle

headers2 = ['Etapa Metodológica Lean', 'Descripción Operativa', 'Tiempo Interno (Máq. Parada)', 'Tiempo Externo (Máq. en Marcha)', 'Tiempo Total de Proceso', '% Reducción vs Línea Base']
for col_idx, h in enumerate(headers2, 1):
    cell = ws2.cell(row=4, column=col_idx, value=h)
    cell.fill = header_fill
    cell.font = font_header
    cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
ws2.row_dimensions[4].height = 26

shingo_stages = [
    ('Etapa 0: Situación Actual (Línea Base)', 'Todas las tareas se realizan con la máquina apagada de forma desordenada.', 45.0, 0.0, 45.0, 0.0),
    ('Etapa 1: Separación Internas y Externas', 'Preparación anticipada de crema, mangas y herramientas 5S antes de apagar.', 32.0, 13.0, 45.0, 0.2889),
    ('Etapa 2: Conversión Internas en Externas', 'Uso de cabezal gemelo premontado y prelavado; lavado fuera de línea.', 20.0, 25.0, 45.0, 0.5556),
    ('Etapa 3: Optimización de Tareas Internas', 'Abrazaderas Tri-Clamp 1/4 vuelta, conexiones push-fit y galgas de color.', 15.0, 20.0, 35.0, 0.6667)
]

for row_idx, stage in enumerate(shingo_stages, 5):
    ws2.row_dimensions[row_idx].height = 24
    for col_idx in range(1, 7):
        cell = ws2.cell(row=row_idx, column=col_idx, value=stage[col_idx-1])
        cell.font = font_regular
        cell.border = thin_border
        if col_idx == 1:
            cell.font = font_bold
            cell.alignment = Alignment(horizontal='left', vertical='center')
        elif col_idx == 2:
            cell.alignment = Alignment(horizontal='left', vertical='center')
        elif col_idx in [3, 4, 5]:
            cell.alignment = Alignment(horizontal='right', vertical='center')
            cell.number_format = '0.0 "min"'
        elif col_idx == 6:
            cell.alignment = Alignment(horizontal='right', vertical='center')
            cell.number_format = '0.0%'
            cell.font = font_bold
            if row_idx == 8: cell.fill = ext_fill

col_widths2 = {1: 32, 2: 50, 3: 20, 4: 22, 5: 18, 6: 22}
for col_idx, width in col_widths2.items():
    ws2.column_dimensions[get_column_letter(col_idx)].width = width


# ==============================================================================
# HOJA 3: IMPACTO FINANCIERO Y CASO DE NEGOCIO (CAPEX CERO)
# ==============================================================================
ws3['A1'] = "MODELO FINANCIERO Y CASO DE NEGOCIO (CAPEX CERO)"
ws3['A1'].font = font_title
ws3['A2'] = "Cuantificación del Retorno de Inversión y Capacidad Productiva Liberada en la Fábrica"
ws3['A2'].font = font_subtitle

headers3 = ['Variable de Negocio / Indicador Financiero', 'Unidad de Medida', 'Valor Base (Actual)', 'Valor Proyecto (SMED)', 'Delta de Mejora (Impacto)', 'Fórmula / Supuesto Operacional']
for col_idx, h in enumerate(headers3, 1):
    cell = ws3.cell(row=4, column=col_idx, value=h)
    cell.fill = header_fill
    cell.font = font_header
    cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
ws3.row_dimensions[4].height = 26

fin_records = [
    ('Tiempo de Parada Rutinaria en Llenadora (CC <=60m)', 'Horas / Mes', 123.52, 74.11, -49.41, 'Meta de reducción del 40.0% sobre paradas rutinarias'),
    ('Horas Netas de Producción Recuperadas', 'Horas / Mes', 0.0, 49.41, 49.41, 'Horas liberadas en el cuello de botella físico'),
    ('Horas Netas Recuperadas Anualizadas', 'Horas / Año', 0.0, 592.92, 592.92, '49.41 h/mes * 12 meses'),
    ('Velocidad Real Mediana Observada', 'Galletas / Hora', 38506, 38506, 0, 'Velocidad de marcha demostrada en Línea 1'),
    ('Galletas Brutas Extra Liberadas', 'Galletas / Mes', 0, 1902631, 1902631, '49.41 h * 38,506 galletas/h'),
    ('Factor de Calidad Vendible (Ajuste por Scrap de Arranque)', '% Vendible', 1.0, 0.985, -0.015, '1.5% de merma en arranque de lote post-cambio'),
    ('Galletas Vendibles Extra al Mes', 'Galletas / Mes', 0, 1874092, 1874092, 'Galletas brutas * 98.5% vendible'),
    ('Galletas Vendibles Extra al Año', 'Galletas / Año', 0, 22489098, 22489098, '1.87 M galletas/mes * 12 meses'),
    ('Cajas de 24 Paquetes Adicionales al Año', 'Cajas (Cases) / Año', 0, 156174, 156174, '22.48 M galletas / 144 galletas por caja'),
    ('Margen de Contribución Unitario Estimado', 'USD / Caja', 3.50, 3.50, 0.0, 'Margen industrial promedio en galletas sandwich'),
    ('Beneficio Bruto Anual por Capacidad Liberada', 'USD / Año', 0.0, 546609, 546609, '156,174 cajas * $3.50 USD/caja'),
    ('Ahorro en Horas Extras de Cuadrilla de Turno', 'USD / Año', 0.0, 35000, 35000, 'Eliminación de turnos de fin de semana para cumplir plan'),
    ('Inversión Requerida (Utillajes Tri-Clamp, Carros 5S, Galgas)', 'USD (Capex)', 0.0, 4800, 4800, 'Capex Cero (Gasto menor OPEX de utillaje rápido)'),
    ('Retorno de Inversión (Payback)', 'Días', 0.0, 3.0, -3.0, '($4,800 / $581,609 anual) * 365 días = 3 días'),
    ('Alternativa de Inversión Tradicional (Nueva Llenadora)', 'USD (Capex)', 250000, 0, -250000, 'Comprar otra línea requeriría $250k y 9 meses de entrega')
]

for row_idx, rec in enumerate(fin_records, 5):
    ws3.row_dimensions[row_idx].height = 22
    for col_idx in range(1, 7):
        val = rec[col_idx-1]
        cell = ws3.cell(row=row_idx, column=col_idx, value=val)
        cell.font = font_regular
        cell.border = thin_border
        
        if col_idx == 1:
            cell.font = font_bold
            cell.alignment = Alignment(horizontal='left', vertical='center')
        elif col_idx == 2:
            cell.alignment = Alignment(horizontal='center', vertical='center')
        elif col_idx in [3, 4, 5]:
            cell.alignment = Alignment(horizontal='right', vertical='center')
            if 'USD' in rec[1]:
                cell.number_format = '$#,##0'
            elif '%' in rec[1]:
                cell.number_format = '0.0%'
            elif 'Galletas' in rec[1] or 'Cajas' in rec[1]:
                cell.number_format = '#,##0'
            else:
                cell.number_format = '0.0'
        elif col_idx == 6:
            cell.alignment = Alignment(horizontal='left', vertical='center')
            cell.font = font_subtitle

col_widths3 = {1: 42, 2: 18, 3: 16, 4: 16, 5: 18, 6: 45}
for col_idx, width in col_widths3.items():
    ws3.column_dimensions[get_column_letter(col_idx)].width = width

excel_out = 'entregables_planta/Matriz_SMED_Reduccion_Setups.xlsx'
wb.save(excel_out)
print(f"Archivo Excel {excel_out} creado con exito total!")
