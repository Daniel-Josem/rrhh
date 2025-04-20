from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QDialog, QSizePolicy, QMessageBox, QComboBox
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

            self.campos = [
                ("Cédula", "cc"),
                ("Nombre", "nombre"),
                ("Apellido", "apellido"),
                ("Puesto", "puesto"),
                ("Salario", "salario"),
                ("Estado", "estado"),
                ("Fecha Ingreso", "fecha_ingreso")
            ]

            self.layout = QVBoxLayout()
            self.form_layout = QHBoxLayout()

            form_left = QVBoxLayout()
            form_right = QVBoxLayout()

            for label_text, key in self.campos:
                label = QLabel(label_text)
                label.setStyleSheet("font-size: 16px;")

                if key == "estado":
                    entry = QComboBox()
                    entry.addItems(["Activo", "Inactivo"])
                else:
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
            self.boton_eliminar.setStyleSheet(self.estilo_boton("#D32F2F", "#B71C1C"))
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
            self.tabla.setColumnCount(7)
            self.tabla.setHorizontalHeaderLabels(["Cédula", "Nombre", "Apellido", "Puesto", "Salario", "Estado", "Ingreso"])
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
            cursor.execute("SELECT cc, nombre, apellido, puesto, salario, estado, fecha_ingreso FROM empleados WHERE estado = 'Activo'")
            for row_idx, row_data in enumerate(cursor.fetchall()):
                self.tabla.insertRow(row_idx)
                for col_idx, value in enumerate(row_data):
                    item = QTableWidgetItem(str(value))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tabla.setItem(row_idx, col_idx, item)
            conn.close()

        def registrar(self):
            datos = []
            for _, key in self.campos:
                if key == "estado":
                    datos.append(self.entries[key].currentText())
                else:
                    datos.append(self.entries[key].text())

            if all(datos):
                try:
                    conn = conectar()
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO empleados (cc, nombre, apellido, puesto, salario, estado, fecha_ingreso) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        datos
                    )
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
            if selected and len(selected) >= 7:
                self.selected_cc = selected[0].text()
                for i, (_, key) in enumerate(self.campos):
                    if key == "estado":
                        idx = self.entries[key].findText(selected[i].text())
                        if idx >= 0:
                            self.entries[key].setCurrentIndex(idx)
                    else:
                        self.entries[key].setText(selected[i].text())
                self.boton_registrar.setText("Actualizar")
                self.boton_registrar.clicked.disconnect(self.registrar)
                self.boton_registrar.clicked.connect(self.actualizar)
            else:
                QMessageBox.warning(self, "Advertencia", "Selecciona una fila completa para editar.")

        def actualizar(self):
            datos = []
            for _, key in self.campos:
                if key == "estado":
                    datos.append(self.entries[key].currentText())
                else:
                    datos.append(self.entries[key].text())

            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE empleados 
                SET nombre = ?, apellido = ?, puesto = ?, salario = ?, estado = ?, fecha_ingreso = ?
                WHERE cc = ?
            """, (datos[1], datos[2], datos[3], datos[4], datos[5], datos[6], datos[0]))
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
            for key, entry in self.entries.items():
                if key == "estado":
                    entry.setCurrentIndex(0)
                else:
                    entry.clear()

        def cerrar(self):
            self.close()
            if self.parent:
                self.parent.show()

    ventana = EmpleadoWindow(parent)
    ventana.exec_()
