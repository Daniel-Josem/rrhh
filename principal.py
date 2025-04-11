from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFrame, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sys
from nomina import nominas
from asistencia import asistencias
from empleado import empleados
from informe_mensual import informes_mensuales

class PrincipalWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Panel Principal")
        self.setGeometry(100, 100, 800, 600)  # Tamaño inicial
        self.setStyleSheet("background-color: #fff8e1;")  # Blanco cremoso
        self.init_ui()
        self.showFullScreen()

    def init_ui(self):
        # Barra superior
        self.barra_superior = QFrame(self)
        self.barra_superior.setStyleSheet("background-color: #0288d1;")  # Azul claro
        self.barra_superior.setGeometry(0, 145, 1500, 80)

        # Título centrado en la barra
        self.titulo = QLabel("RECURSOS HUMANOS", self)
        self.titulo.setFont(QFont("Arial", 24, QFont.Bold))
        self.titulo.setStyleSheet("color: black;")
        self.titulo.setGeometry(500, 30, 400, 40)
        self.titulo.setAlignment(Qt.AlignCenter)

        # Botón Empleados
        self.boton_empleados = QPushButton("Empleados", self)
        self.boton_empleados.setGeometry(50, 160, 200, 50)

        # Botón Informes
        self.boton_informes = QPushButton("Informes", self)
        self.boton_informes.setGeometry(400, 160, 200, 50)

        # Botón Asistencias
        self.boton_asistencias = QPushButton("Asistencias", self)
        self.boton_asistencias.setGeometry(750, 160, 200, 50)

        # Botón Nóminas
        self.boton_nominas = QPushButton("Nóminas", self)
        self.boton_nominas.setGeometry(1110, 160, 200, 50)

        # Botón Cerrar
        self.boton_salir = QPushButton("Cerrar", self)
        self.boton_salir.setGeometry(600, 700, 200, 50)

        # Estilo de botones
        botones = [
            self.boton_nominas,
            self.boton_asistencias,
            self.boton_empleados,
            self.boton_informes,
            self.boton_salir
        ]
        for boton in botones:
            boton.setStyleSheet("""
                QPushButton {
                    background-color: black;
                    color: white;
                    font-size: 16px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #444;
                }
            """)

        # Conexiones
        self.boton_nominas.clicked.connect(self.abrir_nominas)
        self.boton_asistencias.clicked.connect(self.abrir_asistencias)
        self.boton_empleados.clicked.connect(self.abrir_empleados)
        self.boton_informes.clicked.connect(self.abrir_informes)
        self.boton_salir.clicked.connect(self.close)

    # Métodos para cambiar de ventana
    def abrir_nominas(self):
        self.close()
        nominas()

    def abrir_asistencias(self):
        self.close()
        asistencias()

    def abrir_empleados(self):
        self.close()
        empleados()

    def abrir_informes(self):
        self.close()
        informes_mensuales()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = PrincipalWindow()
    ventana.show()
    sys.exit(app.exec_())
