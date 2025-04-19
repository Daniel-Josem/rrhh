from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QMessageBox, QHeaderView, QLineEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sqlite3

color_boton = "#007ACC"
color_fondo = "#fcfcfc"

def conectar():
    return sqlite3.connect("rrhh.db")

class VentanaAsistencia(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Control de Asistencias")
        self.setStyleSheet(f"background-color: {color_fondo};")
        self.showMaximized()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Título
        titulo = QLabel("Registro de Asistencias")
        titulo.setFont(QFont("Arial", 24, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("color: black;")
        layout.addWidget(titulo)

        # Barra de búsqueda
        layout_busqueda = QHBoxLayout()
        self.barra_busqueda = QLineEdit()
        self.barra_busqueda.setPlaceholderText("Buscar por CC, Nombre o Apellido...")
        self.barra_busqueda.setStyleSheet("padding: 6px; font-size: 14px;")
        boton_buscar = QPushButton("Buscar")
        boton_buscar.setStyleSheet(f"""
            QPushButton {{
                background-color: {color_boton};
                color: white;
                padding: 6px 12px;
                border-radius: 6px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: #444;
            }}
        """)
        boton_buscar.clicked.connect(self.buscar_empleados)
        layout_busqueda.addWidget(self.barra_busqueda)
        layout_busqueda.addWidget(boton_buscar)
        layout.addLayout(layout_busqueda)

        # Tabla
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(7)
        self.tabla.setHorizontalHeaderLabels(["ID", "CC", "Nombre", "Apellido", "Fecha", "Entrada", "Salida"])
        self.tabla.horizontalHeader().setStretchLastSection(True)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.tabla)

        # Botones inferiores
        boton_actualizar = QPushButton("Actualizar")
        boton_actualizar.setStyleSheet(f"""
            QPushButton {{
                background-color: {color_boton};
                color: white;
                font-size: 14px;
                padding: 8px 16px;
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background-color: #444;
            }}
        """)
        boton_actualizar.clicked.connect(self.cargar_empleados)

        boton_cerrar = QPushButton("Cerrar")
        boton_cerrar.setStyleSheet(f"""
            QPushButton {{
                background-color: {color_boton};
                color: white;
                font-size: 14px;
                padding: 8px 16px;
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background-color: #444;
            }}
        """)
        boton_cerrar.clicked.connect(self.cerrar_ventana)

        layout_botones = QHBoxLayout()
        layout_botones.addStretch()
        layout_botones.addWidget(boton_actualizar)
        layout_botones.addWidget(boton_cerrar)
        layout_botones.addStretch()
        layout.addLayout(layout_botones)

        self.setLayout(layout)
        self.cargar_empleados()

    def cargar_empleados(self):
        self.cargar_datos()

    def buscar_empleados(self):
        texto = self.barra_busqueda.text().strip()
        if texto:
            self.cargar_datos(filtro=texto)
        else:
            self.cargar_datos()

    def cargar_datos(self, filtro=None):
        try:
            conn = conectar()
            cursor = conn.cursor()
            query_base = """
                SELECT a.id, e.cc, e.nombre, e.apellido, a.fecha, a.hora_entrada, a.hora_salida
                FROM asistencia a
                JOIN empleados e ON a.id_empleado = e.cc
            """
            if filtro:
                query_base += " WHERE e.nombre LIKE ? OR e.apellido LIKE ? OR e.cc LIKE ?"
                parametros = (f"%{filtro}%", f"%{filtro}%", f"%{filtro}%")
                cursor.execute(query_base + " ORDER BY a.fecha DESC", parametros)
            else:
                cursor.execute(query_base + " ORDER BY a.fecha DESC")
            resultados = cursor.fetchall()
            self.tabla.setRowCount(len(resultados))
            for fila, datos in enumerate(resultados):
                for columna, valor in enumerate(datos):
                    self.tabla.setItem(fila, columna, QTableWidgetItem(str(valor)))
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar los datos: {e}")

    def cerrar_ventana(self):
        self.close()
        if self.parent:
            self.parent.show()
