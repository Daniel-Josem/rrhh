from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy, QSpacerItem
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
from nominaus import VentanaNominaUs
from asistenciaus import VentanaAsistenciaUs
import sys

# Colores
color_boton = "#007ACC"
color_fondo = "#fcfcfc"

class PrincipalWindow(QWidget):
    def __init__(self, cc_usuario):
        super().__init__()
        self.setWindowTitle("Panel Usuario")
        self.setStyleSheet(f"background-color: {color_fondo};")
        self.cc_usuario = cc_usuario  # Cédula del usuario logueado
        self.init_ui()

    def init_ui(self):
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(20, 20, 20, 20)
        layout_principal.setSpacing(20)

        # Título
        titulo = QLabel("BIENVENIDO EMPLEADO")
        titulo.setFont(QFont("Arial", 32, QFont.Bold))
        titulo.setStyleSheet("color: black;")
        titulo.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(titulo)

        # Layout de botones
        layout_botones = QHBoxLayout()
        layout_botones.setSpacing(30)

        botones = [
            ("Nomina", self.abrir_nomina, "image/icon_nomina.jpg"),
            ("Asistencias", self.abrir_asistencias, "image/icon_asistencia.jpg")
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

        # Imagen inferior
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

        # Botón de salir
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
        # Crear la ventana de asistencia pero no ocultar la ventana principal
        self.ventana_asistencia = VentanaAsistenciaUs()
        self.ventana_asistencia.showFullScreen()  # Mantener la ventana de asistencia en fullscreen

    def abrir_nomina(self):
        # Crear la ventana de nómina pero no ocultar la ventana principal
        self.ventana_nomina = VentanaNominaUs(cc_usuario=self.cc_usuario)
        self.ventana_nomina.showFullScreen()  # Mantener la ventana de nómina en fullscreen


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = PrincipalWindow(cc_usuario=1045070072)  # Aquí pruebas con una cédula real del usuario
    ventana.showFullScreen()  # Asegurarse de que la ventana principal también esté en fullscreen
    sys.exit(app.exec_())
