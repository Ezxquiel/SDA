
# utils/pdf_generator.py
from fpdf import FPDF
from datetime import datetime
import calendar
from flask import make_response

class AttendanceReport:
    def __init__(self, entrada, salidas, mes=None, año=None):
        self.entrada = entrada
        self.salidas = salidas
        self.mes = mes
        self.año = año
        self.pdf = FPDF()
        self._init_dates()
        
    def _init_dates(self):
        if self.mes is None or self.año is None and self.entrada:
            primera_fecha = datetime.strptime(str(self.entrada[0]['fecha']), '%Y-%m-%d')
            self.mes = self.mes or primera_fecha.month
            self.año = self.año or primera_fecha.year
        else:
            ahora = datetime.now()
            self.mes = self.mes or ahora.month
            self.año = self.año or ahora.year

    def generate(self):
        self.pdf.add_page()
        self._add_header()
        self._add_calendar()
        self._add_tables()
        self._add_footer()
        
        response = make_response(self.pdf.output(dest='S').encode('latin-1'))
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=Reporte_Asistencia_Salida.pdf'
        return response

    def _add_header(self):
        self.pdf.set_font('Arial', 'B', 50)
        self.pdf.set_text_color(200, 200, 200)
        self.pdf.rotate(45, 105, 140)
        self.pdf.text(75, 140, 'ASISTENCIAS')
        self.pdf.rotate(0)
        self.pdf.set_text_color(0, 0, 0)

        self.pdf.image('static/img/logoInaSinFondo.png', x=10, y=10, w=40, h=40)

        self.pdf.set_font('Arial', 'B', 16)
        self.pdf.cell(0, 70, 'Reporte de Asistencia'.encode('latin-1').decode('latin-1'), 0, 1, 'C')

    def _add_calendar(self):
        self.pdf.ln(10)
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.cell(200, 10, 'Calendario de Asistencias'.encode('latin-1').decode('latin-1'), ln=True, align='C')

        fechas_asistidas = {str(entrada['fecha']): True for entrada in self.entrada}
        calendar.setfirstweekday(calendar.SUNDAY)
        mes_cal = calendar.monthcalendar(self.año, self.mes)

        nombres_meses = {
            1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
            5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
            9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
        }

        self.pdf.set_fill_color(51, 122, 183)
        self.pdf.set_text_color(255, 255, 255)
        nombre_mes = nombres_meses[self.mes].encode('latin-1').decode('latin-1')
        self.pdf.cell(0, 10, f"{nombre_mes} {self.año}", 1, 1, 'C', True)

        dias = ['Dom', 'Lun', 'Mar', 'Mié'.encode('latin-1').decode('latin-1'), 
                'Jue', 'Vie', 'Sáb'.encode('latin-1').decode('latin-1')]
        
        self.pdf.set_font('Arial', 'B', 10)
        self.pdf.set_fill_color(240, 240, 240)
        self.pdf.set_text_color(0, 0, 0)
        
        for dia in dias:
            self.pdf.cell(27, 10, dia, 1, 0, 'C', True)
        self.pdf.ln()

        total_asistidos = 0
        total_no_asistidos = 0
        dias_habiles = 0

        self.pdf.set_font('Arial', '', 10)
        for semana in mes_cal:
            for i, dia in enumerate(semana):
                if dia == 0:
                    self.pdf.set_fill_color(245, 245, 245)
                    self.pdf.cell(27, 10, '', 1, 0, 'C', True)
                else:
                    dia_str = f"{self.año}-{self.mes:02d}-{dia:02d}"
                    if i != 0:
                        dias_habiles += 1
                        if dia_str in fechas_asistidas:
                            self.pdf.set_fill_color(223, 240, 216)
                            self.pdf.set_text_color(0, 128, 0)
                            total_asistidos += 1
                        else:
                            self.pdf.set_fill_color(242, 222, 222)
                            self.pdf.set_text_color(169, 68, 66)
                            total_no_asistidos += 1
                    else:
                        self.pdf.set_fill_color(220, 220, 220)
                        self.pdf.set_text_color(128, 128, 128)
                    
                    self.pdf.cell(27, 10, str(dia), 1, 0, 'C', True)
                    self.pdf.set_text_color(0, 0, 0)
            self.pdf.ln()

        self.pdf.ln(10)
        self.pdf.set_font('Arial', 'B', 10)
        self.pdf.set_fill_color(240, 240, 240)
        self.pdf.cell(63, 10, f'Días Hábiles: {dias_habiles}'.encode('latin-1').decode('latin-1'), 1, 0, 'C', True)
        self.pdf.cell(63, 10, f'Días Asistidos: {total_asistidos}'.encode('latin-1').decode('latin-1'), 1, 0, 'C', True)
        self.pdf.cell(64, 10, f'Días No Asistidos: {total_no_asistidos}'.encode('latin-1').decode('latin-1'), 1, 1, 'C', True)

    def _add_tables(self):
        def crear_tabla(titulo, datos, es_entrada=True):
            self.pdf.ln(10)
            self.pdf.set_font('Arial', 'B', 12)
            self.pdf.set_fill_color(51, 122, 183)
            self.pdf.set_text_color(255, 255, 255)
            self.pdf.cell(190, 10, titulo.encode('latin-1').decode('latin-1'), 1, 1, 'C', True)
            
            self.pdf.set_font('Arial', 'B', 8)
            self.pdf.set_fill_color(240, 240, 240)
            self.pdf.set_text_color(0, 0, 0)
            headers = [
                ('ID', 20),
                ('NIE Estudiante', 30),
                ('Nombre', 50),
                ('Fecha', 45),
                ('Hora', 45)
            ]
            
            for header, width in headers:
                self.pdf.cell(width, 10, header.encode('latin-1').decode('latin-1'), 1, 0, 'C', True)
            self.pdf.ln()
            
            self.pdf.set_font('Arial', '', 8)
            for i, dato in enumerate(datos):
                self.pdf.set_fill_color(255, 255, 255) if i % 2 == 0 else self.pdf.set_fill_color(245, 245, 245)
                
                id_key = 'id_entrada' if es_entrada else 'id_salida'
                self.pdf.cell(20, 10, str(dato[id_key]), 1, 0, 'C', True)
                self.pdf.cell(30, 10, str(dato['nie']), 1, 0, 'C', True)
                nombre_codificado = dato['nombre'].encode('latin-1').decode('latin-1')
                self.pdf.cell(50, 10, nombre_codificado, 1, 0, 'L', True)
                self.pdf.cell(45, 10, str(dato['fecha']), 1, 0, 'C', True)
                self.pdf.cell(45, 10, str(dato['hora']), 1, 1, 'C', True)

        crear_tabla('Registro de Entradas', self.entrada, True)
        crear_tabla('Registro de Salidas', self.salidas, False)

    def _add_footer(self):
        self.pdf.set_y(-30)
        self.pdf.set_font('Arial', 'I', 8)
        self.pdf.cell(0, 10, f'Generado el {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}'.encode('latin-1').decode('latin-1'), 0, 0, 'C')