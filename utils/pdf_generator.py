from fpdf import FPDF
from datetime import datetime
import os

class Colors:
    PRIMARY = (41, 128, 185)
    SECONDARY = (241, 196, 15)
    WHITE = (255, 255, 255)
    LIGHT_BLUE = (214, 234, 248)
    HEADER_BLUE = (52, 152, 219)
    DARK_GRAY = (50, 50, 50)

class AttendanceReport:
    def __init__(self, resumen, totales, fecha_inicio, fecha_fin):
        self.resumen = resumen
        self.totales = totales
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)
        self.setup_pdf()

    def setup_pdf(self):
        self.pdf.add_page()
        self.pdf.set_font('Arial', 'B', 16)

    def add_header(self):
        self.pdf.set_fill_color(*Colors.PRIMARY)
        self.pdf.rect(0, 0, 210, 40, 'F')
        self.pdf.image('static/img/logoInaSinFondo.png', x=3, y=3, w=40, h=40)
        self.pdf.set_font('Arial', 'B', 24)
        self.pdf.set_text_color(*Colors.WHITE)
        self.pdf.cell(0, 25, 'Reporte de Asistencia ', 0, 1, 'C')
        
        self.pdf.set_font('Arial', '', 12)
        self.pdf.set_text_color(*Colors.SECONDARY)
        self.pdf.cell(0, 10, f'Período: {self.fecha_inicio} al {self.fecha_fin}', 0, 1, 'C')
        self.pdf.ln(10)

    def format_absence_codes(self, codes_str):
        if not codes_str or codes_str == "[]":
            return "-"
        try:
            codes = eval(codes_str)
            code_count = {}
            for code in codes:
                code_count[code] = code_count.get(code, 0) + 1
            return ", ".join([f"{code}({count})" for code, count in code_count.items()])
        except:
            return codes_str

    def add_totales(self):
        self.pdf.set_fill_color(*Colors.LIGHT_BLUE)
        self.pdf.rect(10, self.pdf.get_y(), 190, 50, 'F')
        
        self.pdf.set_font('Arial', 'B', 14)
        self.pdf.set_text_color(*Colors.PRIMARY)
        self.pdf.cell(0, 10, 'Resumen General', 0, 1)
        
        self.pdf.set_font('Arial', '', 12)
        self.pdf.set_text_color(*Colors.DARK_GRAY)
        
        if self.totales:
            y_start = self.pdf.get_y()
            col_width = 95
                
            self.pdf.set_xy(15, y_start)
            self.pdf.cell(col_width, 8, f'Total Asistidos: {self.totales["total_asistidos"]}', 0)
            self.pdf.set_xy(15, y_start + 8)
            self.pdf.cell(col_width, 8, f'Total Masculino: {self.totales["total_masculino"]}', 0)
            self.pdf.set_xy(15, y_start + 16)
            self.pdf.cell(col_width, 8, f'Total Femenino: {self.totales["total_femenino"]}', 0)

            self.pdf.set_xy(110, y_start)
            self.pdf.cell(col_width, 8, f'Total Inasistidos: {self.totales["total_inasistidos"]}', 0)
            self.pdf.set_xy(110, y_start + 8)

            total_alumnos = self.totales["total_inasistidos"] + self.totales["total_asistidos"]
            self.pdf.cell(col_width, 8, f'Total de Alumnos: {total_alumnos}', 0)

            self.pdf.set_xy(110, y_start + 16)
            self.pdf.cell(col_width, 8, f'% Asistencia: {self.totales["porcentaje_asistencia"]}%', 0)

        self.pdf.ln(30)

    def add_detail_table(self):
        self.pdf.set_font('Arial', 'B', 14)
        self.pdf.set_text_color(*Colors.PRIMARY)
        self.pdf.cell(0, 10, 'Detalle por Sección', 0, 1)
        
        headers = ['Fecha','Año', 'Sección', 'Asist.', 'M', 'F', 'Inasist.', 'Total de alumnos', '% Asist.']
        col_widths = [20, 20, 25, 25, 20, 20, 25, 25, 25]
        
        self.pdf.set_font('Arial', 'B', 10)
        self.pdf.set_fill_color(*Colors.HEADER_BLUE)
        self.pdf.set_text_color(*Colors.WHITE)
        
        for i, header in enumerate(headers):
            self.pdf.cell(col_widths[i], 10, header, 1, 0, 'C', True)
        self.pdf.ln()
        
        self.pdf.set_font('Arial', '', 9)
        self.pdf.set_text_color(*Colors.DARK_GRAY)
        
        for i, row in enumerate(self.resumen):
            fill = Colors.LIGHT_BLUE if i % 2 == 0 else Colors.WHITE
            self.pdf.set_fill_color(*fill)
            
            self.pdf.cell(col_widths[0], 10, str(row['fecha_entrada']), 1, 0, 'C', True)
            self.pdf.cell(col_widths[1], 10, str(row['año']), 1, 0, 'C', True)
            self.pdf.cell(col_widths[2], 10, str(row['seccion']), 1, 0, 'C', True)
            self.pdf.cell(col_widths[3], 10, str(row['total_asistidos']), 1, 0, 'C', True)
            self.pdf.cell(col_widths[4], 10, str(row['total_masculino']), 1, 0, 'C', True)
            self.pdf.cell(col_widths[5], 10, str(row['total_femenino']), 1, 0, 'C', True)
            self.pdf.cell(col_widths[6], 10, str(row['total_inasistidos']), 1, 0, 'C', True)
            total = row['total_inasistidos'] + row['total_asistidos']
            self.pdf.cell(col_widths[7], 10, str(total), 1, 0, 'C', True)
            self.pdf.cell(col_widths[8], 10, f"{row['porcentaje_asistencia']}%", 1, 0, 'C', True)
            self.pdf.ln()

    def add_absence_codes_table(self):
        self.pdf.add_page()
        
        self.pdf.set_font('Arial', 'B', 14)
        self.pdf.set_text_color(*Colors.PRIMARY)
        self.pdf.cell(0, 10, 'Detalle de Códigos de Inasistencia', 0, 1)
        self.pdf.ln(5)
        
        headers = ['Fecha','Año', 'Sección', 'Inasistencias']
        col_widths = [20, 25, 35, 110]
        
        self.pdf.set_font('Arial', 'B', 10)
        self.pdf.set_fill_color(*Colors.HEADER_BLUE)
        self.pdf.set_text_color(*Colors.WHITE)
        
        for i, header in enumerate(headers):
            self.pdf.cell(col_widths[i], 10, header, 1, 0, 'C', True)
        self.pdf.ln()
        
        self.pdf.set_font('Arial', '', 10)
        self.pdf.set_text_color(*Colors.DARK_GRAY)
        
        for i, row in enumerate(self.resumen):
            if row['codigos_inasistidos'] and row['codigos_inasistidos'] != "[]":
                fill = Colors.LIGHT_BLUE if i % 2 == 0 else Colors.WHITE
                self.pdf.set_fill_color(*fill)
                
                codigos = self.format_absence_codes(row['codigos_inasistidos'])
                
                lines = len(codigos) // 60 + 1
                height = max(8, 6 * lines)
                
                self.pdf.cell(col_widths[0], height, str(row['fecha_entrada']), 1, 0, 'C', True)
                self.pdf.cell(col_widths[1], height, str(row['año']), 1, 0, 'C', True)
                self.pdf.cell(col_widths[2], height, str(row['seccion']), 1, 0, 'C', True)
                
                x = self.pdf.get_x()
                y = self.pdf.get_y()
                self.pdf.multi_cell(col_widths[3], 6, codigos, 1, 'C', True)
                
                if i < len(self.resumen) - 1:
                    self.pdf.set_xy(self.pdf.l_margin, y + height)

    def generate(self):
        try:
            self.add_header()
            self.add_totales()
            self.add_detail_table()
            self.add_absence_codes_table()
            
            desktop_path = os.path.expanduser("~/Desktop")
            filename = os.path.join(desktop_path, f'reporte_asistencia_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf')
            self.pdf.output(filename)
            return filename
        except Exception as e:
            raise Exception(f"Error al generar el PDF: {str(e)}")
