# utils/pdf_generator.py
from fpdf import FPDF
from datetime import datetime

class AttendanceReport(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.add_page()
        self.set_font('Arial', 'B', 16)
        
    def header(self):
        # Logo o imagen institucional (opcional)
        # self.image('logo.png', 10, 8, 33)
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Reporte de Asistencia - Turno Matutino', 0, 1, 'C')
        self.ln(10)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}/{{nb}}', 0, 0, 'C')
        
    def set_header_info(self, fecha_inicio, fecha_fin):
        self.set_font('Arial', '', 12)
        self.cell(0, 10, f'Período: {fecha_inicio} - {fecha_fin}', 0, 1, 'L')
        self.ln(5)
        
    def add_table_header(self):
        # Configurar encabezados de la tabla
        self.set_font('Arial', 'B', 10)
        self.set_fill_color(200, 200, 200)
        
        # Definir anchos de columnas
        col_widths = [15, 20, 25, 20, 20, 25, 35, 35]
        headers = ['Año', 'Sección', 'Total\nAsistidos', 'Masculino', 'Femenino', 
                  'Inasistidos', 'Códigos\nInasistidos', 'Códigos\nAsistidos']
        
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 10, header, 1, 0, 'C', True)
        self.ln()
        
        return col_widths
        
    def add_row(self, data, col_widths):
        self.set_font('Arial', '', 9)
        
        # Calcular altura máxima necesaria para la fila
        max_height = 8
        for i, content in enumerate(data):
            if i >= 6:  # Para las columnas de códigos
                needed_height = self.get_string_height(col_widths[i], str(content))
                max_height = max(max_height, needed_height)
        
        # Imprimir cada celda con la altura calculada
        for i, content in enumerate(data):
            align = 'C' if i < 6 else 'L'  # Alineación centrada excepto para códigos
            self.multi_cell(col_widths[i], max_height, str(content), 1, align, False) 
            if i < len(data) - 1:  # Si no es la última celda
                self.set_xy(self.get_x() + col_widths[i], self.get_y() - max_height)
        
        self.ln()
        
    def get_string_height(self, width, txt):
        # Calcula la altura necesaria para el texto
        lines = len(txt.split('\n'))
        return max(8, lines * 4)  # Mínimo 8 pts, o más si hay múltiples líneas

def generate_pdf(resumen, fecha_inicio, fecha_fin):
    try:
        pdf = AttendanceReport()
        pdf.alias_nb_pages()
        
        # Configurar información del encabezado
        pdf.set_header_info(
            fecha_inicio.strftime('%d/%m/%Y'),
            fecha_fin.strftime('%d/%m/%Y')
        )
        
        # Agregar encabezados de la tabla
        col_widths = pdf.add_table_header()
        
        # Agregar filas de datos
        for row in resumen:
            row_data = [
                row[0],  # año
                row[1],  # seccion
                row[2],  # total_asistidos
                row[3],  # masculino
                row[4],  # femenino
                row[5],  # inasistidos
                row[6] if row[6] else 'Ninguno',  # codigos_inasistidos
                row[7] if row[7] else 'Ninguno'   # codigos_asistidos
            ]
            pdf.add_row(row_data, col_widths)
            
        # Generar PDF en memoria
        return pdf.output(dest='S').encode('latin1')
        
    except Exception as e:
        print(f"Error generando PDF: {str(e)}")
        raise