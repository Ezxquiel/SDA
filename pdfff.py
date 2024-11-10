# Clase PDF extendida
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'RESUMEN DE ASISTENCIAS', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Página %s' % self.page_no(), 0, 0, 'C')

    def table_header(self):
        self.set_font('Arial', 'B', 10)
        self.cell(40, 10, 'Sección', 1)
        self.cell(30, 10, 'Asistidos', 1)
        self.cell(20, 10, 'M', 1)
        self.cell(20, 10, 'F', 1)
        self.cell(30, 10, 'Inasistidos', 1)
        self.cell(30, 10, 'Total', 1)
        self.cell(50, 10, 'Cod. Inasistidos', 1)
        self.ln()

    def add_row(self, asistencia):
        self.set_font('Arial', '', 10)
        self.cell(40, 10, f"{asistencia['año']} - {asistencia['seccion']}", 1)
        self.cell(30, 10, str(asistencia['total_asistidos']), 1)
        self.cell(20, 10, str(asistencia['total_masculino']), 1)
        self.cell(20, 10, str(asistencia['total_femenino']), 1)
        self.cell(30, 10, str(asistencia['total_inasistidos']), 1)
        total = asistencia['total'] or asistencia['total_asistidos'] + asistencia['total_inasistidos']
        self.cell(30, 10, str(total), 1)
        codigos = asistencia['codigos_inasistidos'] or 'N/A'
        self.cell(50, 10, codigos, 1)
        self.ln()

# Función para generar el PDF
def generar_pdf(resumen):
    pdf = PDF()
    pdf.add_page()
    pdf.table_header()

    for asistencia in resumen:
        pdf.add_row(asistencia)

    pdf.output('resumen_asistencias.pdf')

# Transformar los datos obtenidos en una lista de diccionarios
resumen_data = [
    {
        'año': asistencia[0],
        'seccion': asistencia[1],
        'total_asistidos': asistencia[2],
        'total_masculino': asistencia[3],
        'total_femenino': asistencia[4],
        'total_inasistidos': asistencia[5],
        'total': asistencia[5] + asistencia[2] if asistencia[5] is not None else asistencia[2],
        'codigos_inasistidos': asistencia[6]
    } 
    for asistencia in resumen
]

# Generar el PDF con los datos procesados
generar_pdf(resumen_data)

# Cerrar conexión
cursor.close()
conexion.close()