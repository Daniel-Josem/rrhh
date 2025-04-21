import sqlite3

# Conectar a la base de datos existente
conn = sqlite3.connect("rrhh.db")
cursor = conn.cursor()

try:
    # 1. Crear nueva tabla con el tipo correcto
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nueva_nominas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cc_empleado INTEGER,
            fecha TEXT,
            salario_base REAL,
            horas_extras_diurnas REAL,
            horas_extras_nocturnas REAL,
            horas_extras_dominicales_diurnas REAL,
            horas_extras_dominicales_nocturnas REAL,
            recargos_nocturnos REAL,
            auxilio_transporte REAL,
            bonificaciones REAL,
            comisiones REAL,
            prestamo REAL,
            salud REAL,
            pension REAL,
            total_devengado REAL,
            total_deducido REAL,
            neto_pagar REAL,
            FOREIGN KEY(cc_empleado) REFERENCES empleados(cc)
        )
    """)

    # 2. Copiar datos desde la tabla original
    cursor.execute("""
        INSERT INTO nueva_nominas (
            cc_empleado, fecha, salario_base, horas_extras_diurnas, horas_extras_nocturnas,
            horas_extras_dominicales_diurnas, horas_extras_dominicales_nocturnas, recargos_nocturnos,
            auxilio_transporte, bonificaciones, comisiones, prestamo, salud, pension,
            total_devengado, total_deducido, neto_pagar
        )
        SELECT
            CAST(cc_empleado AS INTEGER), fecha, salario_base, horas_extras_diurnas, horas_extras_nocturnas,
            horas_extras_dominicales_diurnas, horas_extras_dominicales_nocturnas, recargos_nocturnos,
            auxilio_transporte, bonificaciones, comisiones, prestamo, salud, pension,
            total_devengado, total_deducido, neto_pagar
        FROM nominas
    """)

    # 3. Renombrar tablas
    cursor.execute("ALTER TABLE nominas RENAME TO nominas_backup")
    cursor.execute("ALTER TABLE nueva_nominas RENAME TO nominas")

    conn.commit()
    print("✅ Migración exitosa. Tu tabla 'nominas' ahora tiene cc_empleado como INTEGER.")
except Exception as e:
    print("❌ Error durante la migración:", e)
    conn.rollback()
finally:
    conn.close()
