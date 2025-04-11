import sys
import os
import sqlite3
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QFrame, QMessageBox
)
from PyQt5.QtGui import QPixmap, QFont, QPalette, QBrush
from PyQt5.QtCore import Qt

class LoginAdmin(QWidget):
    def __init__(self):
        super().__init__()

        # Rutas de las imágenes
        self.ruta_fondo = "image/fondo.jpg"
        self.ruta_logo = "image/logo.jpg"

        self.setWindowTitle("Login Administrador")
        self.showFullScreen()

        # Botón salir antes del init_ui
        self.boton_salir = QPushButton("Salir", self)
        self.boton_salir.setStyleSheet("background-color: #555; color: white; padding: 5px;")
        self.boton_salir.setFont(QFont("Arial", 10))
        self.boton_salir.setFixedSize(100, 30)
        self.boton_salir.clicked.connect(self.close)

        self.init_ui()

    def init_ui(self):
        layout_exterior = QVBoxLayout()
        layout_exterior.setAlignment(Qt.AlignCenter)

        layout_centro = QHBoxLayout()
        layout_centro.setAlignment(Qt.AlignCenter)

        frame_login = QFrame()
        frame_login.setFixedSize(400, 600)
        frame_login.setStyleSheet("background-color: white; border-radius: 10px;")

        layout_login = QVBoxLayout()
        layout_login.setAlignment(Qt.AlignTop)
        layout_login.setContentsMargins(30, 30, 30, 30)
        layout_login.setSpacing(15)

        if os.path.exists(self.ruta_logo):
            logo = QPixmap(self.ruta_logo).scaled(180, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label = QLabel()
            logo_label.setPixmap(logo)
            logo_label.setAlignment(Qt.AlignCenter)
            layout_login.addWidget(logo_label)
            layout_login.addSpacing(10)
        else:
            print("No se encontró el logo.")

        titulo = QLabel("Inicio de Sesión")
        titulo.setFont(QFont("Arial", 20, QFont.Bold))
        titulo.setStyleSheet("color: black;")
        titulo.setAlignment(Qt.AlignCenter)
        layout_login.addWidget(titulo)

        layout_login.addSpacing(10)

        usuario_label = QLabel("Usuario:")
        usuario_label.setFont(QFont("Arial", 14))
        usuario_label.setStyleSheet("color: black;")
        layout_login.addWidget(usuario_label)

        self.input_usuario = QLineEdit()
        self.input_usuario.setFont(QFont("Arial", 12))
        self.input_usuario.setStyleSheet("background-color: #f0f0f0; padding: 5px;")
        layout_login.addWidget(self.input_usuario)

        contraseña_label = QLabel("Contraseña:")
        contraseña_label.setFont(QFont("Arial", 14))
        contraseña_label.setStyleSheet("color: black;")
        layout_login.addWidget(contraseña_label)

        self.input_contraseña = QLineEdit()
        self.input_contraseña.setFont(QFont("Arial", 12))
        self.input_contraseña.setEchoMode(QLineEdit.Password)
        self.input_contraseña.setStyleSheet("background-color: #f0f0f0; padding: 5px;")
        layout_login.addWidget(self.input_contraseña)

        layout_login.addSpacing(20)

        boton_ingresar = QPushButton("Ingresar")
        boton_ingresar.setStyleSheet("background-color: black; color: white; padding: 10px;")
        boton_ingresar.setFont(QFont("Arial", 12))
        boton_ingresar.clicked.connect(self.verificar_login)
        layout_login.addWidget(boton_ingresar)

        frame_login.setLayout(layout_login)
        layout_centro.addWidget(frame_login)
        layout_exterior.addLayout(layout_centro)
        self.setLayout(layout_exterior)

        self.actualizar_fondo()

    def resizeEvent(self, event):
        if hasattr(self, 'ruta_fondo'):
            self.actualizar_fondo()
        if hasattr(self, 'boton_salir'):
            self.boton_salir.move(self.width() - 110, 20)

    def actualizar_fondo(self):
        if os.path.exists(self.ruta_fondo):
            fondo = QPixmap(self.ruta_fondo).scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            palette = QPalette()
            palette.setBrush(QPalette.Window, QBrush(fondo))
            self.setPalette(palette)
        else:
            print("No se encontró la imagen de fondo.")

    def verificar_login(self):
        usuario = self.input_usuario.text()
        contraseña = self.input_contraseña.text()

        if not usuario or not contraseña:
            QMessageBox.warning(self, "Campos vacíos", "Por favor completa ambos campos")
            return

        try:
            conexion = sqlite3.connect("rrhh.db")
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM usuario_rrhh WHERE usuario = ? AND contraseña = ?", (usuario, contraseña))
            resultado = cursor.fetchone()

            if resultado:
                try:
                    subprocess.Popen([sys.executable, "principal.py"])
                    self.close()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo ejecutar principal.py:\n{e}")
            else:
                QMessageBox.critical(self, "Acceso denegado", "Usuario o contraseña incorrectos")

            cursor.close()
            conexion.close()

        except sqlite3.Error as err:
            QMessageBox.critical(self, "Error", f"No se pudo conectar a la base de datos:\n{err}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = LoginAdmin()
    ventana.show()
    sys.exit(app.exec_())
