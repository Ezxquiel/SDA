CREATE DATABASE IF NOT EXISTS asistencia; -- Crea la base de datos si no existe
USE asistencia; -- Selecciona la base de datos para usarla


-- Tabla usuarios
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,           -- Identificador único autoincremental para cada usuario
    nombre VARCHAR(250) NOT NULL UNIQUE,         -- Nombre de usuario, único y obligatorio
    contraseña VARCHAR(250) NOT NULL,            -- Contraseña del usuario, obligatoria
    rango VARCHAR(250) NOT NULL                  -- Rango del usuario (por ejemplo: 'admin', 'estudiante', 'profesor')
);

-- Tabla seccion
CREATE TABLE seccion (
    año INT NOT NULL,                           -- Año escolar, no permite valores nulos
    seccion CHAR(1) NOT NULL,                   -- Sección (un solo carácter), no permite valores nulos
    especialidad VARCHAR(50) NOT NULL,          -- Nombre de la especialidad, longitud ajustada a 50 caracteres
    PRIMARY KEY (año, seccion)                  -- Clave primaria compuesta (año y sección)
);

-- Tabla materias
CREATE TABLE materias (
    id_materia INT AUTO_INCREMENT PRIMARY KEY,  -- Identificador único autoincremental para cada materia
    materia VARCHAR(70) NOT NULL UNIQUE         -- Nombre de la materia, no permite valores nulos y debe ser único
);

-- Tabla justificaciones
CREATE TABLE justificaciones (
    id_justificacion INT AUTO_INCREMENT PRIMARY KEY, -- Identificador único autoincremental para cada justificación
    tipo VARCHAR(100) NOT NULL,                      -- Tipo de justificación, campo obligatorio
    descripcion TEXT,                                -- Detalle de la justificación, permite valores largos
    fecha_permiso DATE                               -- Fecha del permiso otorgado
);

-- Tabla estudiantes
CREATE TABLE estudiantes (
    id_estudiante INT AUTO_INCREMENT PRIMARY KEY,    -- Identificador único autoincremental para cada estudiante
    nombre VARCHAR(200) NOT NULL,                    -- Nombre completo del estudiante, no permite valores nulos
    nie VARCHAR(15) UNIQUE NOT NULL,                 -- Número de identificación único del estudiante
    edad TINYINT UNSIGNED,                           -- Edad del estudiante, solo permite valores positivos
    genero ENUM('M', 'F') DEFAULT 'M',               -- Género del estudiante, restringido a 'M' o 'F', con valor por defecto 'M'
    año INT NOT NULL,                                -- Año escolar del estudiante
    seccion CHAR(1) NOT NULL,                        -- Sección del estudiante                         
    especialidad VARCHAR(50),                        -- Especialidad del estudiante (opcional)
    codigo CHAR(4),                                  -- Código del estudiante (longitud fija de 4 caracteres)
    FOREIGN KEY (año, seccion) REFERENCES seccion(año, seccion) ON DELETE CASCADE 
    -- Clave foránea que vincula el año y la sección del estudiante con la tabla 'seccion'. 
    -- Se eliminan los estudiantes si la sección es eliminada.
);

-- Tabla entrada
CREATE TABLE entrada (
    id_entrada INT AUTO_INCREMENT PRIMARY KEY,       -- Identificador único autoincremental para cada entrada
    nie VARCHAR(15) NOT NULL,                        -- Número de identificación del estudiante que registró la entrada
    fecha_entrada DATE NOT NULL,                     -- Fecha de la entrada
    hora_entrada TIME NOT NULL,                      -- Hora de la entrada
    FOREIGN KEY (nie) REFERENCES estudiantes(nie) ON DELETE CASCADE 
    -- Clave foránea que asegura que cada entrada esté vinculada a un estudiante. 
    -- Si se elimina el estudiante, se eliminan sus registros de entrada.
);

-- Tabla salida
CREATE TABLE salida (
    id_salida INT AUTO_INCREMENT PRIMARY KEY,        -- Identificador único autoincremental para cada salida
    nie VARCHAR(15) NOT NULL,                        -- Número de identificación del estudiante que registró la salida
    fecha_salida DATE NOT NULL,                      -- Fecha de la salida
    hora_salida TIME NOT NULL,                       -- Hora de la salida
    FOREIGN KEY (nie) REFERENCES estudiantes(nie) ON DELETE CASCADE 
    -- Clave foránea que asegura que cada salida esté vinculada a un estudiante. 
    -- Si se elimina el estudiante, se eliminan sus registros de salida.
);

-- Tabla asistencia_materia
CREATE TABLE asistencia_materia (
    id_asistencia_materia INT AUTO_INCREMENT PRIMARY KEY, -- Identificador único autoincremental para cada asistencia
    id_estudiante INT NOT NULL,                           -- Referencia al estudiante por ID
    id_materia INT NOT NULL,                              -- Referencia a la materia impartida
    fecha_clase DATE NOT NULL,                            -- Fecha de la clase
    hora_clase TIME NOT NULL,                             -- Hora de la clase
    maestro VARCHAR(250),
    estado ENUM('Presente', 'Ausente', 'Justificado') NOT NULL, -- Estado de la asistencia
    id_justificacion INT,                                 -- Referencia a la justificación, si aplica
    FOREIGN KEY (id_justificacion) REFERENCES justificaciones(id_justificacion) ON DELETE SET NULL, 
    -- Si se elimina una justificación, se deja el campo como NULL en lugar de eliminar el registro.
    FOREIGN KEY (id_materia) REFERENCES materias(id_materia) ON DELETE CASCADE, 
    -- Si se elimina una materia, se eliminan las asistencias relacionadas.
    FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id_estudiante) ON DELETE CASCADE 
    -- Si se elimina un estudiante, se eliminan sus registros de asistencia.
);

-- Insertar entradas solo para los NIES que terminan en 9, 4 o 7
INSERT INTO entrada (nie, fecha_entrada, hora_entrada) 
SELECT nie, CURDATE(), CURTIME()  -- Aquí usamos la fecha y hora actuales
FROM estudiantes
WHERE nie LIKE '%9' OR nie LIKE '%4' OR nie LIKE '%7';

USE asistencia;
INSERT INTO entrada (nie, fecha_entrada, hora_entrada) 
SELECT nie, '2025-01-16', '13:00:00'
FROM estudiantes
WHERE nie LIKE '%9' OR nie LIKE '%4' OR nie LIKE '%7';




USE asistencia;
truncate table materias;

select * from asistencias_materias;


INSERT INTO asistencia_materia (
    id_estudiante,
    materia,
    fecha_clase,
    hora_clase,
    maestro,
    estado,
    id_justificacion
)
VALUES
    (1, -- ID de estudiante (debe existir en la tabla `estudiantes`)
     'ciencias', -- ID de materia (debe existir en la tabla `materias`)
     '2025-01-16', -- Fecha de la clase
     '08:00:00', -- Hora de la clase
     'Profesor Pérez', -- Nombre del maestro
     'Presente', -- Estado de la asistencia ('Presente', 'Ausente', 'Justificado')
     NULL -- ID de justificación (puede ser NULL si no aplica)
    );


INSERT INTO materias (materia) VALUES 
('ciencias');

UPDATE materias
SET materia = ciencias
WHERE id_materia = 3;
