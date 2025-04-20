-- Crear tabla empleados
CREATE TABLE IF NOT EXISTS empleados (
    cc INT PRIMARY KEY,
    nombre CHAR NOT NULL,
    apellido CHAR NOT NULL,
    puesto TEXT,
    salario INT,
    estado TEXT NOT NULL DEFAULT 'Activo',
    fecha_ingreso TEXT
);

-- Crear tabla asistencia
CREATE TABLE IF NOT EXISTS asistencia (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_empleado INT NOT NULL,
    fecha TEXT NOT NULL,
    hora_entrada TEXT,
    hora_salida TEXT,
    estado TEXT NOT NULL,
    FOREIGN KEY (id_empleado) REFERENCES empleados(cc)
);

-- Crear tabla usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario CHAR NOT NULL UNIQUE,
    contraseña TEXT NOT NULL
);

-- Crear tabla usuario_rrhh
CREATE TABLE IF NOT EXISTS usuario_rrhh (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario CHAR NOT NULL,
    contraseña TEXT NOT NULL
);

-- Insertar usuarios de ejemplo en usuario_rrhh
INSERT INTO usuario_rrhh (usuario, contraseña) VALUES
('admin', '1234'),
('usuario1', 'pass1'),
('usuario2', 'pass2');

-- Insertar empleados de prueba
INSERT INTO empleados (cc, nombre, apellido, puesto, salario, estado, fecha_ingreso) VALUES
(1046692761, 'Juan', 'Pérez', 'Contador', 1500000, 'ACTIVO','2023-03-01'),
(1046692762, 'Ana' ,'Gómez', 'Recepcionista', 1000000,'ACTIVO','2022-11-15'),
(1046692763, 'Carlos',' Ruiz', 'Técnico', 1200000, 'ACTIVO', '2024-01-10');

-- Insertar asistencias de prueba
INSERT INTO asistencia (id_empleado, fecha, hora_entrada, hora_salida, estado) VALUES
(1046692761, '2025-04-15', '08:00', '16:00', 'ACTIVO'),
(1046692762, '2025-04-15', '08:15', '16:20','ACTIVO'),
(1046692763, '2025-04-15', '09:00', '17:00','ACTIVO');
