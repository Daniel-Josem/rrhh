from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sqlite3
from datetime import datetime

class VentanaAsistenciaUs(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Asistencia")
        self.setStyleSheet("background-color: #fcfcfc;")
        self.init_ui()

    def init_ui(self):
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(40, 40, 40, 40)
        layout_principal.setSpacing(30)

        titulo = QLabel("Registro de Asistencia")
        titulo.setFont(QFont("Arial", 32, QFont.Bold))
        titulo.setStyleSheet("color: black;")
        titulo.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(titulo)

        self.input_cedula = QLineEdit()
        self.input_cedula.setPlaceholderText("Ingrese su cédula")
        self.input_cedula.setFont(QFont("Arial", 16))
        self.input_cedula.setAlignment(Qt.AlignCenter)
        self.input_cedula.setStyleSheet("padding: 10px; border: 2px solid #007ACC; border-radius: 8px;")
        layout_principal.addWidget(self.input_cedula)

        botones_layout = QHBoxLayout()
        botones_layout.setSpacing(20)

        boton_entrada = QPushButton("Marcar Entrada")
        boton_entrada.setFont(QFont("Arial", 16, QFont.Bold))
        boton_entrada.setFixedHeight(50)
        boton_entrada.setStyleSheet("background-color: #007ACC; color: white; border-radius: 8px;")
        boton_entrada.clicked.connect(self.marcar_entrada)
        botones_layout.addWidget(boton_entrada)

        boton_salida = QPushButton("Marcar Salida")
        boton_salida.setFont(QFont("Arial", 16, QFont.Bold))
        boton_salida.setFixedHeight(50)
        boton_salida.setStyleSheet("background-color: #007ACC; color: white; border-radius: 8px;")
        boton_salida.clicked.connect(self.marcar_salida)
        botones_layout.addWidget(boton_salida)

        layout_principal.addLayout(botones_layout)

        boton_salir = QPushButton("Cerrar")
        boton_salir.setFont(QFont("Arial", 14))
        boton_salir.setStyleSheet("background-color: #007ACC; color: white; padding: 10px; border-radius: 6px;")
        boton_salir.clicked.connect(self.close)
        layout_principal.addWidget(boton_salir, alignment=Qt.AlignCenter)

    def mostrar_alerta(self, mensaje):
        alerta = QMessageBox()
        alerta.setWindowTitle("Aviso")
        alerta.setText(mensaje)
        alerta.setIcon(QMessageBox.Warning)
        alerta.exec_()

    def mostrar_info(self, mensaje):
        info = QMessageBox()
        info.setWindowTitle("Éxito")
        info.setText(mensaje)
        info.setIcon(QMessageBox.Information)
        info.exec_()

    def marcar_entrada(self):
        cedula = self.input_cedula.text()
        if not cedula.isdigit():
            self.mostrar_alerta("Por favor, ingrese una cédula válida.")
            return

        conexion = sqlite3.connect("rrhh.db")
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM empleados WHERE cc = ?", (cedula,))
        empleado = cursor.fetchone()

        if empleado:
            fecha = datetime.now().strftime("%Y-%m-%d")
            hora_entrada = datetime.now().strftime("%H:%M")
            cursor.execute("INSERT INTO asistencia (id_empleado, fecha, hora_entrada, estado) VALUES (?, ?, ?, ?)",
                           (cedula, fecha, hora_entrada, "Entrada"))
            conexion.commit()
            self.mostrar_info("Entrada registrada correctamente.")
        else:
            self.mostrar_alerta("Cédula incorrecta.")

        conexion.close()

    def marcar_salida(self):
        cedula = self.input_cedula.text()
        if not cedula.isdigit():
            self.mostrar_alerta("Por favor, ingrese una cédula válida.")
            return

        conexion = sqlite3.connect("rrhh.db")
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM empleados WHERE cc = ?", (cedula,))
        empleado = cursor.fetchone()

        if empleado:
            fecha = datetime.now().strftime("%Y-%m-%d")
            hora_salida = datetime.now().strftime("%H:%M")
            cursor.execute("UPDATE asistencia SET hora_salida = ?, estado = 'Salida' WHERE id_empleado = ? AND fecha = ?",
                           (hora_salida, cedula, fecha))
            conexion.commit()
            self.mostrar_info("Salida registrada correctamente.")
        else:
            self.mostrar_alerta("Cédula incorrecta.")

        conexion.close()
