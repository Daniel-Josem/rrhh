from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QDialog, QSizePolicy, QMessageBox
)
from PyQt5.QtCore import Qt
import sqlite3

def conectar():
    return sqlite3.connect("rrhh.db")

def ventana_empleados(parent=None):
    class EmpleadoWindow(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setWindowTitle("Gestión de Empleados")
            self.setStyleSheet("background-color: #fcfcfc;")
            self.showFullScreen()
            self.parent = parent

            self.entries = {}
            # Agregamos 'cc' como primer campo
            self.campos = [("Cédula", "cc"), ("Nombre", "nombre"), ("Puesto", "puesto"), ("Salario", "salario"), ("Fecha Ingreso", "fecha_ingreso")]

            self.layout = QVBoxLayout()
            self.form_layout = QHBoxLayout()

            form_left = QVBoxLayout()
            form_right = QVBoxLayout()

            for label_text, key in self.campos:
                label = QLabel(label_text)
                label.setStyleSheet("font-size: 16px;")
                entry = QLineEdit()
                entry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                entry.setStyleSheet("padding: 5px; font-size: 14px;")
                self.entries[key] = entry
                form_left.addWidget(label)
                form_right.addWidget(entry)

            self.form_layout.addLayout(form_left)
            self.form_layout.addLayout(form_right)

            self.layout.addLayout(self.form_layout)

            # Botones de acción
            self.boton_registrar = QPushButton("Registrar")
            self.boton_registrar.setStyleSheet(self.estilo_boton("#007ACC", "#005A9E"))
            self.boton_registrar.setFixedWidth(150)
            self.boton_registrar.clicked.connect(self.registrar)

            self.boton_editar = QPushButton("Editar")
            self.boton_editar.setStyleSheet(self.estilo_boton("#007ACC", "#005A9E"))
            self.boton_editar.setFixedWidth(150)
            self.boton_editar.clicked.connect(self.editar)

            self.boton_eliminar = QPushButton("Eliminar")
            self.boton_eliminar.setStyleSheet(self.estilo_boton("#D9534F", "#C9302C"))
            self.boton_eliminar.setFixedWidth(150)
            self.boton_eliminar.clicked.connect(self.eliminar)

            self.boton_cerrar = QPushButton("Cerrar")
            self.boton_cerrar.setStyleSheet(self.estilo_boton("#007ACC", "#005A9E"))
            self.boton_cerrar.setFixedWidth(150)
            self.boton_cerrar.clicked.connect(self.cerrar)

            layout_botones = QHBoxLayout()
            layout_botones.addWidget(self.boton_registrar)
            layout_botones.addWidget(self.boton_editar)
            layout_botones.addWidget(self.boton_eliminar)
            layout_botones.addWidget(self.boton_cerrar)
            self.layout.addLayout(layout_botones)

            # Tabla de empleados
            self.tabla = QTableWidget()
            self.tabla.setColumnCount(5)
            self.tabla.setHorizontalHeaderLabels(["Cédula", "Nombre", "Puesto", "Salario", "Ingreso"])
            self.tabla.horizontalHeader().setStretchLastSection(True)
            self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.layout.addWidget(self.tabla)

            self.setLayout(self.layout)
            self.cargar()

        def estilo_boton(self, color, hover):
            return f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    padding: 10px;
                    font-size: 14px;
                    border-radius: 5px;
                }}
                QPushButton:hover {{
                    background-color: {hover};
                }}
            """

        def cargar(self):
            self.tabla.setRowCount(0)
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT cc, nombre, puesto, salario, fecha_ingreso FROM empleados")
            for row_idx, row_data in enumerate(cursor.fetchall()):
                self.tabla.insertRow(row_idx)
                for col_idx, value in enumerate(row_data):
                    self.tabla.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
            conn.close()

        def registrar(self):
            datos = [self.entries[k].text() for _, k in self.campos]
            if all(datos):
                try:
                    conn = conectar()
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO empleados (cc, nombre, puesto, salario, fecha_ingreso) VALUES (?, ?, ?, ?, ?)", datos)
                    conn.commit()
                    conn.close()
                    self.cargar()
                    self.limpiar_formulario()
                except sqlite3.IntegrityError:
                    QMessageBox.warning(self, "Error", "Ya existe un empleado con esa cédula.")
            else:
                QMessageBox.warning(self, "Campos incompletos", "Por favor, completa todos los campos.")

        def editar(self):
            selected = self.tabla.selectedItems()
            if selected and len(selected) >= 5:
                self.selected_cc = selected[0].text()
                for i, (_, key) in enumerate(self.campos):
                    self.entries[key].setText(selected[i].text())
                self.boton_registrar.setText("Actualizar")
                self.boton_registrar.clicked.disconnect(self.registrar)
                self.boton_registrar.clicked.connect(self.actualizar)
            else:
                QMessageBox.warning(self, "Advertencia", "Selecciona una fila completa para editar.")

        def actualizar(self):
            datos = [self.entries[k].text() for _, k in self.campos]
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE empleados 
                SET nombre = ?, puesto = ?, salario = ?, fecha_ingreso = ?
                WHERE cc = ?
            """, (datos[1], datos[2], datos[3], datos[4], datos[0]))
            conn.commit()
            conn.close()
            self.cargar()
            self.boton_registrar.setText("Registrar")
            self.boton_registrar.clicked.disconnect(self.actualizar)
            self.boton_registrar.clicked.connect(self.registrar)
            self.limpiar_formulario()

        def eliminar(self):
            selected = self.tabla.selectedItems()
            if selected:
                cc = selected[0].text()
                conn = conectar()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM empleados WHERE cc = ?", (cc,))
                conn.commit()
                conn.close()
                self.cargar()
            else:
                QMessageBox.warning(self, "Advertencia", "Selecciona una fila para eliminar.")

        def limpiar_formulario(self):
            for entry in self.entries.values():
                entry.clear()

        def cerrar(self):
            self.close()
            if self.parent:
                self.parent.show()

    ventana = EmpleadoWindow(parent)
    ventana.exec_()
