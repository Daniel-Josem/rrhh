from PyQt5.QtWidgets import (
    QDialog, QLabel, QComboBox, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QWidget, QScrollArea
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sqlite3


def conectar():
    return sqlite3.connect("rrhh.db")


def formatear_pesos(valor):
    return f"{int(round(valor)):,}".replace(",", ".")


def ventana_nomina(parent=None):
    class NominaWindow(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setWindowTitle("Cálculo de Nómina")
            self.setStyleSheet("background-color: #fcfcfc;")
            self.showMaximized()

            main_layout = QVBoxLayout()
            main_layout.setSpacing(10)
            main_layout.setContentsMargins(10, 10, 10, 10)
            main_layout.setAlignment(Qt.AlignTop)

            titulo = QLabel("NÓMINA")
            titulo.setFont(QFont("Arial", 24, QFont.Bold))
            titulo.setAlignment(Qt.AlignCenter)
            main_layout.addWidget(titulo)

            fila_superior = QHBoxLayout()
            fila_superior.setSpacing(10)

            self.cb_empleado = QComboBox()
            self.cb_empleado.setFixedHeight(28)

            self.le_salario_base = QLineEdit()
            self.le_salario_base.setReadOnly(True)
            self.le_salario_base.setFixedHeight(25)

            fila_superior.addWidget(QLabel("EMPLEADO"))
            fila_superior.addWidget(self.cb_empleado)
            fila_superior.addStretch()
            fila_superior.addWidget(QLabel("SALARIO BASE"))
            fila_superior.addWidget(self.le_salario_base)
            main_layout.addLayout(fila_superior)

            # TABLA DE HORAS INGRESADAS
            self.horas_extra_labels = [
                "Horas extras diurnas",
                "Horas extras nocturnas",
                "Horas extras dominicales diurnas",
                "Horas extras dominicales nocturnas",
                "Recargos nocturnos"
            ]
            self.horas_inputs = {}

            tabla_horas = QTableWidget(len(self.horas_extra_labels), 2)
            tabla_horas.setHorizontalHeaderLabels(["CONCEPTO", "CANTIDAD HORAS"])
            tabla_horas.verticalHeader().setVisible(False)
            tabla_horas.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            for i, label in enumerate(self.horas_extra_labels):
                tabla_horas.setItem(i, 0, QTableWidgetItem(label))
                entrada = QLineEdit()
                entrada.setPlaceholderText("0")
                entrada.setFixedHeight(25)
                entrada.textChanged.connect(self.calcular_nomina)
                tabla_horas.setCellWidget(i, 1, entrada)
                tabla_horas.setRowHeight(i, 30)
                self.horas_inputs[label] = entrada

            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            tabla_contenedor = QWidget()
            layout_scroll = QVBoxLayout(tabla_contenedor)
            layout_scroll.addWidget(tabla_horas)
            scroll.setWidget(tabla_contenedor)
            scroll.setMaximumHeight(200)
            main_layout.addWidget(scroll)

            # TABLA DE RESULTADOS
            self.etiquetas = [
                "AUXILIO DE TRANSPORTE", "BONIFICACIONES", "PRESTAMO",
                "HORAS EXTRAS DIURNA", "HORAS EXTRAS NOCTURNAS", "RECARGOS",
                "HORAS EXTRAS DOMINICALES DIURNAS", "HORAS EXTRAS DOMINICALES NOCTURNAS",
                "SALUD", "PENSION", "COMISIONES",
                "TOTAL DEVENGADO", "TOTAL DEDUCIDO", "NETO A PAGAR"
            ]
            self.campos = {}

            self.tabla = QTableWidget(len(self.etiquetas), 2)
            self.tabla.setHorizontalHeaderLabels(["CONCEPTO", "VALOR"])
            self.tabla.verticalHeader().setVisible(False)
            self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            for i, etiqueta in enumerate(self.etiquetas):
                self.tabla.setItem(i, 0, QTableWidgetItem(etiqueta))
                campo = QLineEdit()
                campo.setFixedHeight(25)
                if etiqueta in ["TOTAL DEVENGADO", "TOTAL DEDUCIDO", "NETO A PAGAR", "SALUD", "PENSION",
                                "HORAS EXTRAS DIURNA", "HORAS EXTRAS NOCTURNAS",
                                "RECARGOS", "HORAS EXTRAS DOMINICALES DIURNAS", "HORAS EXTRAS DOMINICALES NOCTURNAS"]:
                    campo.setReadOnly(True)
                campo.textChanged.connect(self.calcular_nomina)
                self.tabla.setCellWidget(i, 1, campo)
                self.tabla.setRowHeight(i, 30)
                self.campos[etiqueta] = campo

            main_layout.addWidget(self.tabla)

            cerrar_btn = QPushButton("Cerrar")
            cerrar_btn.setFixedHeight(50)
            cerrar_btn.clicked.connect(self.volver_a_principal)
            cerrar_btn.setStyleSheet(self.estilo_boton("#007ACC", "#005A9E"))
            main_layout.addWidget(cerrar_btn, alignment=Qt.AlignCenter)

            self.setLayout(main_layout)
            self.cargar_empleados()

        def estilo_boton(self, color_base, color_hover):
            return f"""
            QPushButton {{
                background-color: {color_base};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-size: 16px;
            }}
            QPushButton:hover {{
                background-color: {color_hover};
            }}
            """

        def cargar_empleados(self):
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT cc, nombre, apellido, salario FROM empleados")
            self.lista_empleados = cursor.fetchall()
            for emp in self.lista_empleados:
                cc, nombre, apellido, salario = emp
                self.cb_empleado.addItem(f"{cc} - {nombre} {apellido}")
            self.cb_empleado.currentIndexChanged.connect(self.actualizar_salario)
            if self.lista_empleados:
                self.actualizar_salario()
            conn.close()

        def actualizar_salario(self):
            idx = self.cb_empleado.currentIndex()
            if idx >= 0:
                salario = float(self.lista_empleados[idx][3])
                self.le_salario_base.setText(formatear_pesos(salario))

                salud = salario * 0.04
                pension = salario * 0.04
                auxilio_de_transporte = 200000 if salario <= 2602600 else 0

                self.campos["SALUD"].setText(formatear_pesos(salud))
                self.campos["PENSION"].setText(formatear_pesos(pension))
                self.campos["AUXILIO DE TRANSPORTE"].setText(formatear_pesos(auxilio_de_transporte))

                self.calcular_nomina()

        def calcular_nomina(self):
            try:
                salario_str = self.le_salario_base.text().replace(".", "")
                salario = float(salario_str or 0)
                valor_hora = salario / 230 if salario > 0 else 0

                def obtener_valor(campo):
                    texto = self.campos[campo].text().replace(".", "")
                    return float(texto) if texto else 0

                def calcular_horas(label_input, campo_resultado, factor):
                    texto = self.horas_inputs[label_input].text().strip()
                    horas = float(texto) if texto.replace(".", "").isdigit() else 0
                    valor = horas * valor_hora * factor
                    self.campos[campo_resultado].setText(formatear_pesos(valor))
                    return valor

                valores = {
                    "AUXILIO DE TRANSPORTE": obtener_valor("AUXILIO DE TRANSPORTE"),
                    "BONIFICACIONES": obtener_valor("BONIFICACIONES"),
                    "COMISIONES": obtener_valor("COMISIONES"),
                    "HORAS EXTRAS DIURNA": calcular_horas("Horas extras diurnas", "HORAS EXTRAS DIURNA", 1.25),
                    "HORAS EXTRAS NOCTURNAS": calcular_horas("Horas extras nocturnas", "HORAS EXTRAS NOCTURNAS", 1.75),
                    "RECARGOS": calcular_horas("Recargos nocturnos", "RECARGOS", 1.35),
                    "HORAS EXTRAS DOMINICALES DIURNAS": calcular_horas(
                        "Horas extras dominicales diurnas", "HORAS EXTRAS DOMINICALES DIURNAS", 2.0),
                    "HORAS EXTRAS DOMINICALES NOCTURNAS": calcular_horas(
                        "Horas extras dominicales nocturnas", "HORAS EXTRAS DOMINICALES NOCTURNAS", 2.5)
                }

                total_devengado = salario + sum(valores.values())
                self.campos["TOTAL DEVENGADO"].setText(formatear_pesos(total_devengado))

                prestamo = obtener_valor("PRESTAMO")
                salud = obtener_valor("SALUD")
                pension = obtener_valor("PENSION")
                total_deducido = prestamo + salud + pension
                self.campos["TOTAL DEDUCIDO"].setText(formatear_pesos(total_deducido))

                neto = total_devengado - total_deducido
                self.campos["NETO A PAGAR"].setText(formatear_pesos(neto))

            except Exception as e:
                print("Error en el cálculo:", e)

        def volver_a_principal(self):
            self.close()
            if parent:
                parent.show()

    ventana = NominaWindow(parent)
    ventana.show()
