from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QFileDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sqlite3
from fpdf import FPDF

# Colores
color_boton = "#007ACC"
color_fondo = "#fcfcfc"

class VentanaNominaUs(QWidget):
    def __init__(self, parent=None, cc_usuario=None):
        super().__init__(parent)
        self.setWindowTitle("Nómina")
        self.setStyleSheet(f"background-color: {color_fondo};")
        self.cc_usuario = cc_usuario  # Cedula del usuario logueado
        self.init_ui()

    def init_ui(self):
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(40, 40, 40, 40)
        layout_principal.setSpacing(30)

        # Título
        titulo = QLabel("Nómina del Empleado")
        titulo.setFont(QFont("Arial", 32, QFont.Bold))
        titulo.setStyleSheet("color: black;")
        titulo.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(titulo)

        # Layout centrado para la tabla
        tabla_layout = QHBoxLayout()
        tabla_layout.setAlignment(Qt.AlignCenter)

        # Tabla de nómina
        self.tabla_nomina = QTableWidget()
        self.tabla_nomina.setRowCount(0)  # Inicialmente sin filas
        self.tabla_nomina.setColumnCount(2)  # Dos columnas: "Concepto" y "Valor"
        self.tabla_nomina.setHorizontalHeaderLabels(["Concepto", "Valor"])
        self.tabla_nomina.setStyleSheet("background-color: white; border: 1px solid #ddd;")
        
        # Hacer la tabla más pequeña (ajustar tamaño de celdas)
        self.tabla_nomina.setFixedWidth(600)  # Ancho fijo para la tabla
        self.tabla_nomina.setColumnWidth(0, 250)  # Ancho de la primera columna
        self.tabla_nomina.setColumnWidth(1, 250)  # Ancho de la segunda columna

        tabla_layout.addWidget(self.tabla_nomina)
        layout_principal.addLayout(tabla_layout)

        # Botones
        botones_layout = QHBoxLayout()
        botones_layout.setSpacing(30)

        boton_generar_pdf = QPushButton("Generar PDF de Nómina")
        boton_generar_pdf.setMinimumHeight(50)
        boton_generar_pdf.setFont(QFont("Arial", 14, QFont.Bold))
        boton_generar_pdf.setStyleSheet(f"background-color: {color_boton}; color: white; border-radius: 10px;")
        boton_generar_pdf.clicked.connect(self.generar_pdf)
        botones_layout.addWidget(boton_generar_pdf)

        boton_salir = QPushButton("Cerrar")
        boton_salir.setMinimumHeight(50)
        boton_salir.setFont(QFont("Arial", 14, QFont.Bold))
        boton_salir.setStyleSheet(f"background-color: {color_boton}; color: white; border-radius: 10px;")
        boton_salir.clicked.connect(self.close)
        botones_layout.addWidget(boton_salir)

        layout_principal.addLayout(botones_layout)

        self.cargar_nomina()

    def cargar_nomina(self):
        if not self.cc_usuario:
            self.tabla_nomina.setRowCount(1)
            self.tabla_nomina.setItem(0, 0, QTableWidgetItem("Error"))
            self.tabla_nomina.setItem(0, 1, QTableWidgetItem("No se proporcionó una cédula de empleado."))
            return

        conexion = sqlite3.connect("rrhh.db")
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT e.nombre, e.apellido, e.puesto, e.salario, n.fecha, n.salario_base, 
                   n.horas_extras_diurnas, n.horas_extras_nocturnas, n.horas_extras_dominicales_diurnas, 
                   n.horas_extras_dominicales_nocturnas, n.recargos_nocturnos, n.auxilio_transporte, 
                   n.bonificaciones, n.comisiones, n.prestamo, n.salud, n.pension, 
                   n.total_devengado, n.total_deducido, n.neto_pagar
            FROM empleados e
            JOIN nominas n ON e.cc = n.cc_empleado
            WHERE e.cc = ?
        """, (self.cc_usuario,))

        datos = cursor.fetchone()
        conexion.close()

        if datos:
            conceptos = [
                ("Empleado", f"{datos[0]} {datos[1]}"),
                ("Puesto", datos[2]),
                ("Salario", f"${datos[3]}"),
                ("Fecha de nómina", datos[4]),
                ("Salario Base", f"${datos[5]}"),
                ("Horas Extras Diurnas", f"${datos[6]}"),
                ("Horas Extras Nocturnas", f"${datos[7]}"),
                ("Horas Extras Dominicales Diurnas", f"${datos[8]}"),
                ("Horas Extras Dominicales Nocturnas", f"${datos[9]}"),
                ("Recargos Nocturnos", f"${datos[10]}"),
                ("Auxilio de Transporte", f"${datos[11]}"),
                ("Bonificaciones", f"${datos[12]}"),
                ("Comisiones", f"${datos[13]}"),
                ("Préstamo", f"${datos[14]}"),
                ("Salud", f"${datos[15]}"),
                ("Pensión", f"${datos[16]}"),
                ("Total Devengado", f"${datos[17]}"),
                ("Total Deducido", f"${datos[18]}"),
                ("Neto a Pagar", f"${datos[19]}")
            ]

            self.tabla_nomina.setRowCount(len(conceptos))

            for i, (concepto, valor) in enumerate(conceptos):
                self.tabla_nomina.setItem(i, 0, QTableWidgetItem(concepto))
                self.tabla_nomina.setItem(i, 1, QTableWidgetItem(valor))

        else:
            self.tabla_nomina.setRowCount(1)
            self.tabla_nomina.setItem(0, 0, QTableWidgetItem("Error"))
            self.tabla_nomina.setItem(0, 1, QTableWidgetItem("No se encontró información de nómina para este empleado."))

    def generar_pdf(self):
        if not self.cc_usuario:
            return

        conexion = sqlite3.connect("rrhh.db")
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT e.nombre, e.apellido, e.puesto, e.salario, n.fecha, n.salario_base, 
                   n.horas_extras_diurnas, n.horas_extras_nocturnas, n.horas_extras_dominicales_diurnas, 
                   n.horas_extras_dominicales_nocturnas, n.recargos_nocturnos, n.auxilio_transporte, 
                   n.bonificaciones, n.comisiones, n.prestamo, n.salud, n.pension, 
                   n.total_devengado, n.total_deducido, n.neto_pagar
            FROM empleados e
            JOIN nominas n ON e.cc = n.cc_empleado
            WHERE e.cc = ?
        """, (self.cc_usuario,))

        datos = cursor.fetchone()
        conexion.close()

        if not datos:
            return

        # Creación del PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Nómina del Empleado", ln=True, align='C')
        pdf.ln(10)
        pdf.cell(200, 10, f"Nombre: {datos[0]} {datos[1]}", ln=True)
        pdf.cell(200, 10, f"Puesto: {datos[2]}", ln=True)
        pdf.cell(200, 10, f"Salario: ${datos[3]}", ln=True)

        # Datos adicionales de nómina
        conceptos = [
            ("Salario Base", f"${datos[5]}"),
            ("Horas Extras Diurnas", f"${datos[6]}"),
            ("Horas Extras Nocturnas", f"${datos[7]}"),
            ("Horas Extras Dominicales Diurnas", f"${datos[8]}"),
            ("Horas Extras Dominicales Nocturnas", f"${datos[9]}"),
            ("Recargos Nocturnos", f"${datos[10]}"),
            ("Auxilio de Transporte", f"${datos[11]}"),
            ("Bonificaciones", f"${datos[12]}"),
            ("Comisiones", f"${datos[13]}"),
            ("Préstamo", f"${datos[14]}"),
            ("Salud", f"${datos[15]}"),
            ("Pensión", f"${datos[16]}"),
            ("Total Devengado", f"${datos[17]}"),
            ("Total Deducido", f"${datos[18]}"),
            ("Neto a Pagar", f"${datos[19]}")
        ]

        for concepto, valor in conceptos:
            pdf.cell(200, 10, f"{concepto}: {valor}", ln=True)

        # Diálogo para guardar el PDF
        ruta, _ = QFileDialog.getSaveFileName(self, "Guardar PDF", "nomina_empleado.pdf", "PDF Files (*.pdf)")
        if ruta:
            pdf.output(ruta)
