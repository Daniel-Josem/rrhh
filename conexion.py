import sqlite3

def conectar():
    conn = sqlite3.connect('rrhh.db')  # Utilizamos tu base de datos existente rrhh.db
    return conn
