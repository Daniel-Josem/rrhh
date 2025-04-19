from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout, QSizePolicy, QSpacerItem
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
import sys
import sqlite3
from asistencia import VentanaAsistencia
from empleado import ventana_empleados 
from nomina import ventana_nomina 
from informe import ventana_informe  # ✅ Importación corregida

# Colores fijos
color_boton = "#007ACC"
color_fondo = "#fcfcfc"

def conectar():
    return sqlite3.connect("rrhh.db")

class PrincipalWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Panel Principal")
        self.setStyleSheet(f"background-color: {color_fondo};")
        self.init_ui()
        self.showFullScreen()

    def init_ui(self):
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(20, 20, 20, 20)
        layout_principal.setSpacing(20)

        titulo = QLabel("RECURSOS HUMANOS")
        titulo.setFont(QFont("Arial", 32, QFont.Bold))
        titulo.setStyleSheet("color: black;")
        titulo.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(titulo)

        layout_botones = QHBoxLayout()
        layout_botones.setSpacing(30)

        botones = [
            ("Nomina", self.abrir_nomina, "image/icon_nomina.jpg"),
            ("Gestion de empleados", self.abrir_empleados, "image/icon_gestion.jpg"),
            ("Asistencias", self.abrir_asistencias, "image/icon_asistencia.jpg"),
            ("Informe Mensual", self.abrir_informe, "image/icon_informe.jpg")
        ]

        for texto, funcion, ruta_imagen in botones:
            layout_boton = QVBoxLayout()
            layout_boton.setSpacing(10)

            icono = QLabel()
            pixmap = QPixmap(ruta_imagen)
            if not pixmap.isNull():
                icono.setPixmap(pixmap.scaled(70, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                icono.setText("❌")
                icono.setStyleSheet("color: red; font-size: 16px;")
            icono.setAlignment(Qt.AlignCenter)

            boton = QPushButton(texto)
            boton.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            boton.setFixedHeight(80)
            boton.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color_boton};
                    color: white;
                    font-size: 14px;
                    border-radius: 6px;
                }}
                QPushButton:hover {{
                    background-color: #444;
                }}
            """)
            boton.clicked.connect(funcion)

            layout_boton.addWidget(icono)
            layout_boton.addWidget(boton)
            layout_botones.addLayout(layout_boton)

        layout_principal.addLayout(layout_botones)

        imagen_inferior = QLabel()
        pixmap_inferior = QPixmap("image/banner_inferior.jpg")
        if not pixmap_inferior.isNull():
            imagen_inferior.setPixmap(pixmap_inferior.scaledToWidth(1000, Qt.SmoothTransformation))
        else:
            imagen_inferior.setText("No se encontró 'banner_inferior.jpg'")
            imagen_inferior.setStyleSheet("color: red; font-size: 16px;")
        imagen_inferior.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(imagen_inferior)

        layout_principal.addSpacerItem(QSpacerItem(50, 100, QSizePolicy.Minimum, QSizePolicy.Expanding))

        boton_salir = QPushButton("Cerrar")
        boton_salir.setFixedHeight(50)
        boton_salir.setFixedWidth(100)
        boton_salir.setStyleSheet(f"""
            QPushButton {{
                background-color: {color_boton};
                color: white;
                font-size: 14px;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: #444;
            }}
        """)
        boton_salir.clicked.connect(self.close)
        layout_principal.addWidget(boton_salir, alignment=Qt.AlignCenter)

    def abrir_asistencias(self):
        self.hide()
        self.ventana_asistencia = VentanaAsistencia(self)
        self.ventana_asistencia.show()

    def abrir_empleados(self):
        self.hide()
        ventana_empleados(self)

    def abrir_nomina(self):
        self.hide()
        ventana_nomina(parent=self)

    def abrir_informe(self):
        self.hide()
        self.ventana_informe = ventana_informe(self)  # ✅ Cambio aquí
        self.ventana_informe.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = PrincipalWindow()
    ventana.show()
    sys.exit(app.exec_())
