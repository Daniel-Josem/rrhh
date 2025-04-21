import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QSpinBox, QTableWidget, QTableWidgetItem, QMessageBox,
    QFileDialog, QHeaderView
)
from reportlab.lib.pagesizes import landscape
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


class ventana_informe(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Informe de Nómina")
        self.setStyleSheet("background-color: #fcfcfc;")
        self.showFullScreen()

        layout = QVBoxLayout()

        self.titulo = QLabel("Informe Mensual de Nómina")
        self.titulo.setFont(QFont("Arial", 20, QFont.Bold))
        self.titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.titulo)

        filtro_layout = QHBoxLayout()

        filtro_layout.addWidget(QLabel("Mes:"))
        self.mes_combo = QComboBox()
        self.mes_combo.addItems([
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ])
        filtro_layout.addWidget(self.mes_combo)

        filtro_layout.addWidget(QLabel("Año:"))
        self.ano_spin = QSpinBox()
        self.ano_spin.setRange(2000, 2100)
        self.ano_spin.setValue(datetime.now().year)
        filtro_layout.addWidget(self.ano_spin)

        self.generar_btn = QPushButton("Generar Informe")
        self.generar_btn.setStyleSheet("background-color: #007ACC; color: white; padding: 8px 16px; border-radius: 6px;")
        self.generar_btn.clicked.connect(self.generar_informe)
        filtro_layout.addWidget(self.generar_btn)

        self.exportar_btn = QPushButton("Exportar a PDF")
        self.exportar_btn.setStyleSheet("background-color: #28A745; color: white; padding: 8px 16px; border-radius: 6px;")
        self.exportar_btn.clicked.connect(self.exportar_pdf)
        filtro_layout.addWidget(self.exportar_btn)

        layout.addLayout(filtro_layout)

        self.tabla = QTableWidget()
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.tabla)

        self.lbl_totales = QLabel("Totales del Mes")
        self.lbl_totales.setAlignment(Qt.AlignCenter)
        self.lbl_totales.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(self.lbl_totales)

        self.totales_tabla = QTableWidget()
        self.totales_tabla.setColumnCount(4)
        self.totales_tabla.setHorizontalHeaderLabels([
            "Total Empleados", "Nómina Bruta", "Total Préstamos", "Neto a Pagar"
        ])
        self.totales_tabla.setRowCount(1)
        self.totales_tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.totales_tabla)

        self.btn_cerrar = QPushButton("Cerrar")
        self.btn_cerrar.setStyleSheet("background-color: #007ACC; color: white; padding: 6px 12px; border-radius: 10px;")
        self.btn_cerrar.clicked.connect(self.close)
        layout.addWidget(self.btn_cerrar, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def generar_informe(self):
        mes = self.mes_combo.currentIndex() + 1
        ano = self.ano_spin.value()

        conn = sqlite3.connect("rrhh.db")
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT n.cc_empleado, e.nombre, e.apellido, e.puesto, 
                       n.salario_base, 
                       n.horas_extras_diurnas + n.horas_extras_nocturnas + 
                       n.horas_extras_dominicales_diurnas + n.horas_extras_dominicales_nocturnas AS horas_extras,
                       n.recargos_nocturnos, n.auxilio_transporte, n.prestamo, 
                       n.total_devengado, n.neto_pagar, n.fecha
                FROM nominas n
                JOIN empleados e ON n.cc_empleado = e.cc
                WHERE strftime('%m', n.fecha) = ? AND strftime('%Y', n.fecha) = ?
            """, (f"{mes:02d}", str(ano)))

            datos = cursor.fetchall()

            columnas = [
                "Cédula", "Nombre", "Apellido", "Puesto", "Salario Base",
                "Horas Extras", "Recargos", "Aux. Transporte", "Préstamo",
                "Total Devengado", "Neto a Pagar", "Fecha"
            ]

            self.tabla.setRowCount(len(datos))
            self.tabla.setColumnCount(len(columnas))
            self.tabla.setHorizontalHeaderLabels(columnas)

            total_nomina = 0
            total_prestamos = 0
            total_neto = 0

            for row_idx, row_data in enumerate(datos):
                for col_idx, value in enumerate(row_data):
                    if isinstance(value, (float, int)):
                        item = QTableWidgetItem(f"{value:,.0f}".replace(",", "."))
                        item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    else:
                        item = QTableWidgetItem(str(value))
                    self.tabla.setItem(row_idx, col_idx, item)

                total_nomina += row_data[9] if row_data[9] else 0
                total_prestamos += row_data[8] if row_data[8] else 0
                total_neto += row_data[10] if row_data[10] else 0

            self.totales_tabla.setItem(0, 0, QTableWidgetItem(str(len(datos))))
            self.totales_tabla.setItem(0, 1, QTableWidgetItem(f"{total_nomina:,.0f}".replace(",", ".")))
            self.totales_tabla.setItem(0, 2, QTableWidgetItem(f"{total_prestamos:,.0f}".replace(",", ".")))
            self.totales_tabla.setItem(0, 3, QTableWidgetItem(f"{total_neto:,.0f}".replace(",", ".")))

            self.titulo.setText(f"Informe de Nómina - {self.mes_combo.currentText()} {ano}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo generar el informe: {e}")
        finally:
            conn.close()

    def exportar_pdf(self):
        path, _ = QFileDialog.getSaveFileName(self, "Guardar Informe como PDF", "", "PDF Files (*.pdf)")
        if not path:
            return

        try:
            # Crear documento PDF en horizontal
            doc = SimpleDocTemplate(path, pagesize=landscape(letter), rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20)
            elementos = []

            estilos = getSampleStyleSheet()
            titulo = Paragraph("Informe Mensual de Nómina", estilos['Title'])
            elementos.append(titulo)
            elementos.append(Spacer(1, 12))

            # Crear tabla de nómina
            headers = [self.tabla.horizontalHeaderItem(i).text() for i in range(self.tabla.columnCount())]
            data = [headers]

            for row in range(self.tabla.rowCount()):
                fila = []
                for col in range(self.tabla.columnCount()):
                    item = self.tabla.item(row, col)
                    fila.append(item.text() if item else "")
                data.append(fila)

            tabla_nomina = Table(data, repeatRows=1)
            tabla_nomina.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 7),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
            ]))

            elementos.append(tabla_nomina)
            elementos.append(Spacer(1, 20))

            # Crear tabla de totales
            total_headers = [self.totales_tabla.horizontalHeaderItem(i).text() for i in range(self.totales_tabla.columnCount())]
            total_data = [total_headers]
            total_row = []

            for i in range(self.totales_tabla.columnCount()):
                item = self.totales_tabla.item(0, i)
                total_row.append(item.text() if item else "")
            total_data.append(total_row)

            tabla_totales = Table(total_data, repeatRows=1)
            tabla_totales.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 7),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
            ]))

            elementos.append(Paragraph("Totales del Mes", estilos['Heading2']))
            elementos.append(tabla_totales)

            # Generar PDF
            doc.build(elementos)
            QMessageBox.information(self, "Éxito", "Informe exportado correctamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo exportar el informe: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = ventana_informe()
    ventana.show()
    sys.exit(app.exec_())
