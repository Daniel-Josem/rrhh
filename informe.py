from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QHBoxLayout, QComboBox, QPushButton, QMessageBox, QHeaderView, QFileDialog
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sqlite3
import calendar
from datetime import datetime
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


def conectar():
    return sqlite3.connect("rrhh.db")

MESES_ES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

class ventana_informe(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle("Informe Mensual de Nómina")
        self.setStyleSheet("background-color: #fcfcfc;")
        self.showFullScreen()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.titulo = QLabel("Informe Mensual de Nómina")
        self.titulo.setFont(QFont("Arial", 20, QFont.Bold))
        self.titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.titulo)

        filtro_layout = QHBoxLayout()

        self.cb_mes = QComboBox()
        self.cb_mes.addItems(MESES_ES)

        self.cb_ano = QComboBox()
        self.cb_ano.addItems([str(ano) for ano in range(2023, datetime.now().year + 1)])

        boton_generar = QPushButton("Generar Informe")
        boton_generar.setStyleSheet("background-color: #007ACC; color: white; padding: 8px 16px; border-radius: 6px;")
        boton_generar.clicked.connect(self.generar_informe)

        boton_pdf = QPushButton("Exportar a PDF")
        boton_pdf.setStyleSheet("background-color: #28A745; color: white; padding: 8px 16px; border-radius: 6px;")
        boton_pdf.clicked.connect(self.exportar_pdf)

        filtro_layout.addWidget(QLabel("Mes:"))
        filtro_layout.addWidget(self.cb_mes)
        filtro_layout.addWidget(QLabel("Año:"))
        filtro_layout.addWidget(self.cb_ano)
        filtro_layout.addWidget(boton_generar)
        filtro_layout.addWidget(boton_pdf)

        layout.addLayout(filtro_layout)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(11)
        self.tabla.setHorizontalHeaderLabels([
            "Cédula", "Nombre", "Apellido", "Puesto", "Días Trabajados", "Salario Base",
            "Horas Extras", "Recargos", "Aux. Transporte", "Préstamos", "Neto a Pagar"
        ])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.tabla)

        # Título de la segunda tabla
        self.lbl_totales_titulo = QLabel("Totales del Mes")
        self.lbl_totales_titulo.setAlignment(Qt.AlignCenter)
        self.lbl_totales_titulo.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(self.lbl_totales_titulo)

        # Segunda tabla para totales del mes
        self.tabla_totales = QTableWidget()
        self.tabla_totales.setRowCount(1)
        self.tabla_totales.setColumnCount(4)
        self.tabla_totales.setHorizontalHeaderLabels([
            "Total Empleados", "Nómina Bruta", "Total Préstamos", "Neto a Pagar"
        ])
        self.tabla_totales.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.tabla_totales)

        boton_regresar = QPushButton("Cerrar")
        boton_regresar.setStyleSheet("background-color: #007ACC; color: white; padding: 6px 12px; border-radius: 10px;")
        boton_regresar.clicked.connect(self.volver_al_menu)
        layout.addWidget(boton_regresar, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def generar_informe(self):
        mes = self.cb_mes.currentIndex() + 1
        ano = int(self.cb_ano.currentText())
        nombre_mes_es = MESES_ES[mes - 1]

        try:
            conn = conectar()
            cursor = conn.cursor()

            fecha_inicio = f"{ano:04d}-{mes:02d}-01"
            fecha_fin = f"{ano:04d}-{mes:02d}-{calendar.monthrange(ano, mes)[1]}"

            cursor.execute("""
                SELECT 
                    e.cc, e.nombre, e.apellido, e.puesto, COUNT(a.fecha) as dias_trabajados,
                    e.salario, 
                    IFNULL(SUM(a.horas_extra), 0), 
                    IFNULL(SUM(a.recargos), 0),
                    IFNULL(SUM(a.aux_transporte), 0),
                    IFNULL(SUM(a.prestamo), 0),
                    IFNULL(SUM(a.neto_pagar), 0)
                FROM asistencia a
                JOIN empleados e ON a.id_empleado = e.cc
                WHERE a.fecha BETWEEN ? AND ?
                GROUP BY e.cc
            """, (fecha_inicio, fecha_fin))

            resultados = cursor.fetchall()
            self.tabla.setRowCount(len(resultados))

            self.total_empleados = len(resultados)
            self.total_bruto = 0
            self.total_prestamos = 0
            self.total_neto = 0

            for fila, datos in enumerate(resultados):
                for columna, valor in enumerate(datos):
                    if columna >= 5:
                        item = QTableWidgetItem(f"{int(round(valor)):,}".replace(",", "."))
                        item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    else:
                        item = QTableWidgetItem(str(valor))
                    self.tabla.setItem(fila, columna, item)

                self.total_bruto += datos[5]
                self.total_prestamos += datos[9]
                self.total_neto += datos[10]

            self.titulo.setText(f"Informe de Nómina - {nombre_mes_es} {ano}")

            # Llenar la segunda tabla
            self.tabla_totales.setItem(0, 0, QTableWidgetItem(str(self.total_empleados)))
            self.tabla_totales.setItem(0, 1, QTableWidgetItem(f"${self.total_bruto:,.0f}".replace(",", ".")))
            self.tabla_totales.setItem(0, 2, QTableWidgetItem(f"${self.total_prestamos:,.0f}".replace(",", ".")))
            self.tabla_totales.setItem(0, 3, QTableWidgetItem(f"${self.total_neto:,.0f}".replace(",", ".")))

            conn.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo generar el informe: {e}")

    def exportar_pdf(self):
        if self.tabla.rowCount() == 0:
            QMessageBox.warning(self, "Sin datos", "Primero debe generar el informe.")
            return

        nombre_mes = MESES_ES[self.cb_mes.currentIndex()]
        ano = self.cb_ano.currentText()
        nombre_archivo, _ = QFileDialog.getSaveFileName(self, "Guardar como", f"informe_{nombre_mes}_{ano}.pdf", "PDF (*.pdf)")
        if not nombre_archivo:
            return

        try:
            doc = SimpleDocTemplate(nombre_archivo, pagesize=landscape(letter))
            elementos = []

            estilos = getSampleStyleSheet()
            titulo = Paragraph(f"<b>Informe de Nómina - {nombre_mes} {ano}</b>", estilos["Title"])
            elementos.append(titulo)

            data = [[self.tabla.horizontalHeaderItem(i).text() for i in range(self.tabla.columnCount())]]
            for row in range(self.tabla.rowCount()):
                fila = []
                for col in range(self.tabla.columnCount()):
                    item = self.tabla.item(row, col)
                    fila.append(item.text() if item else "")
                data.append(fila)

            tabla_pdf = Table(data)
            tabla_pdf.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#007ACC")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
            ]))
            elementos.append(tabla_pdf)

            resumen = Paragraph(
                f"<b>Total empleados:</b> {self.total_empleados} | "
                f"<b>Nómina Bruta:</b> ${self.total_bruto:,.0f} | "
                f"<b>Total Préstamos:</b> ${self.total_prestamos:,.0f} | "
                f"<b>Neto a Pagar:</b> ${self.total_neto:,.0f}".replace(",", "."),
                estilos["Normal"]
            )
            elementos.append(resumen)

            doc.build(elementos)
            QMessageBox.information(self, "PDF generado", f"Informe exportado como:\n{nombre_archivo}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo generar el PDF:\n{e}")

    def volver_al_menu(self):
        if self.parent:
            self.close()
            self.parent.show()
        else:
            self.close()
