CREATE DATABASE IF NOT EXISTS asistencia;
USE asistencia;

-- Tabla padres
CREATE TABLE padres (
    id INT AUTO_INCREMENT PRIMARY KEY,           -- AUTO_INCREMENT para autoincremento en MySQL
    nombre VARCHAR(60) NOT NULL,
    numero VARCHAR(15) UNIQUE NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL,
    dui VARCHAR(15) UNIQUE NOT NULL              -- Asegurar que el DUI sea único
);

-- Tabla seccion
CREATE TABLE seccion (
    año INT NOT NULL,
    seccion VARCHAR(1) NOT NULL,
    especialidad VARCHAR(20) NOT NULL,           -- Ya no es única
    PRIMARY KEY (año, seccion)                   -- Clave primaria compuesta
);

-- Tabla estudiantes
CREATE TABLE estudiantes (
    id INT AUTO_INCREMENT PRIMARY KEY,           -- AUTO_INCREMENT para autoincremento en MySQL
    nombre VARCHAR(200) NOT NULL,
    nie VARCHAR(15) UNIQUE NOT NULL,
    edad TINYINT,
    genero VARCHAR(1),
    año INT NOT NULL,
    seccion VARCHAR(1) NOT NULL,
    dui VARCHAR(15),
    especialidad VARCHAR(20),
    codigo VARCHAR(4),
    FOREIGN KEY (año, seccion) REFERENCES seccion(año, seccion),   -- Clave compuesta referenciada
    FOREIGN KEY (dui) REFERENCES padres(dui) ON DELETE SET NULL,   -- Clave foránea, elimina DUI si el padre se borra
    FOREIGN KEY (año, seccion) REFERENCES seccion(año, seccion)    -- Clave compuesta a seccion
);

-- Tabla entrada
CREATE TABLE entrada (
    id_entrada INT AUTO_INCREMENT PRIMARY KEY,   -- AUTO_INCREMENT para autoincremento en MySQL
    nie VARCHAR(15) NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    FOREIGN KEY (nie) REFERENCES estudiantes(nie) ON DELETE CASCADE -- Borra registros si el estudiante se borra
);

-- Tabla salida
CREATE TABLE salida (
    id_salida INT AUTO_INCREMENT PRIMARY KEY,    -- AUTO_INCREMENT para autoincremento en MySQL
    nie VARCHAR(15) NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    FOREIGN KEY (nie) REFERENCES estudiantes(nie) ON DELETE CASCADE -- Borra registros si el estudiante se borra
);



UPDATE seccion
SET año = 1, seccion = 'A'
WHERE especialidad = 'Contabilidad';

-- eliminar llaves primarias y foraneas
ALTER TABLE seccion DROP INDEX unique_especialidad;

ALTER TABLE estudiantes DROP FOREIGN KEY estudiantes_ibfk_3;

ALTER TABLE estudiantes 
ADD CONSTRAINT estudiantes_ibfk_3 
FOREIGN KEY (especialidad) REFERENCES seccion(especialidad);


INSERT INTO seccion (año, seccion, especialidad) VALUES
(1, 'A', 'Contabilidad'),
(1, 'B', 'Contabilidad'),
(1, 'C', 'Software'),
(1, 'D', 'Software'),
(1, 'E', 'Salud'),
(1, 'F', 'Salud'),
(1, 'G', 'Electrónica'),
(1, 'H', 'General'),
(1, 'I', 'General'),
(1, 'J', 'General'),
(1, 'K', 'General');

-- Insertar para el año 2 (siguiendo la secuencia para C, D, E)
INSERT INTO seccion (año, seccion, especialidad) VALUES
(2, 'A', 'Contabilidad'),
(2, 'B', 'Contabilidad'),
(2, 'C', 'Software'),
(2, 'D', 'Software'),
(2, 'E', 'Software'),
(2, 'F', 'Salud'),
(2, 'G', 'Salud'),
(2, 'H', 'Electrónica'),
(2, 'I', 'General'),
(2, 'J', 'General'),
(2, 'K', 'General'),
(2, 'L', 'General');

-- Sección 2A (General)
INSERT INTO estudiantes (nombre, nie, edad, año, seccion, dui, codigo, genero) VALUES
('Juan Pérez', '10321', 18, 2, 'A', '12345678-9', '2A01', 'M'),
('Marta Sánchez', '10322', 19, 2, 'A', '12345678-9', '2A02', 'F'),
('Carlos González', '10323', 18, 2, 'A', '12345678-9', '2A03', 'M'),
('Raquel Pérez', '10324', 19, 2, 'A', '12345678-9', '2A04', 'F'),
('José Rodríguez', '10325', 18, 2, 'A', '12345678-9', '2A05', 'M'),
('Lucía López', '10326', 19, 2, 'A', '12345678-9', '2A06', 'F'),
('David Martínez', '10327', 18, 2, 'A', '12345678-9', '2A07', 'M'),
('Cristina Sánchez', '10328', 19, 2, 'A', '12345678-9', '2A08', 'F'),
('Tomás González', '10329', 18, 2, 'A', '12345678-9', '2A09', 'M'),
('Patricia Rodríguez', '10330', 19, 2, 'A', '12345678-9', '2A10', 'F'),
('José Pérez', '10331', 18, 2, 'A', '12345678-9', '2A11', 'M'),
('Raquel González', '10332', 19, 2, 'A', '12345678-9', '2A12', 'F'),
('Carlos López', '10333', 18, 2, 'A', '12345678-9', '2A13', 'M'),
('Verónica Sánchez', '10334', 19, 2, 'A', '12345678-9', '2A14', 'F'),
('David Pérez', '10335', 18, 2, 'A', '12345678-9', '2A15', 'M'),
('Lucía Rodríguez', '10336', 19, 2, 'A', '12345678-9', '2A16', 'F'),
('José Martínez', '10337', 18, 2, 'A', '12345678-9', '2A17', 'M'),
('Patricia Pérez', '10338', 19, 2, 'A', '12345678-9', '2A18', 'F'),
('Carlos Rodríguez', '10339', 18, 2, 'A', '12345678-9', '2A19', 'M'),
('Raquel Martínez', '10340', 19, 2, 'A', '12345678-9', '2A20', 'F'),
('David González', '10341', 18, 2, 'A', '12345678-9', '2A21', 'M'),
('Marta López', '10342', 19, 2, 'A', '12345678-9', '2A22', 'F'),
('Tomás Pérez', '10343', 18, 2, 'A', '12345678-9', '2A23', 'M'),
('Cristina Pérez', '10344', 19, 2, 'A', '12345678-9', '2A24', 'F'),
('José Sánchez', '10345', 18, 2, 'A', '12345678-9', '2A25', 'M'),
('Verónica Pérez', '10346', 19, 2, 'A', '12345678-9', '2A26', 'F'),
('David Rodríguez', '10347', 18, 2, 'A', '12345678-9', '2A27', 'M'),
('Patricia González', '10348', 19, 2, 'A', '12345678-9', '2A28', 'F'),
('Carlos Pérez', '10349', 18, 2, 'A', '12345678-9', '2A29', 'M'),
('Raquel Sánchez', '10350', 19, 2, 'A', '12345678-9', '2A30', 'F');

-- Sección 2B (General)
INSERT INTO estudiantes (nombre, nie, edad, año, seccion, dui, codigo, genero) VALUES
('Juan Rodríguez', '10351', 18, 2, 'B', '12345678-9', '2B01', 'M'),
('Patricia Sánchez', '10352', 19, 2, 'B', '12345678-9', '2B02', 'F'),
('Carlos Pérez', '10353', 18, 2, 'B', '12345678-9', '2B03', 'M'),
('Raquel González', '10354', 19, 2, 'B', '12345678-9', '2B04', 'F'),
('José Sánchez', '10355', 18, 2, 'B', '12345678-9', '2B05', 'M'),
('Lucía Rodríguez', '10356', 19, 2, 'B', '12345678-9', '2B06', 'F'),
('David Pérez', '10357', 18, 2, 'B', '12345678-9', '2B07', 'M'),
('Cristina López', '10358', 19, 2, 'B', '12345678-9', '2B08', 'F'),
('Tomás González', '10359', 18, 2, 'B', '12345678-9', '2B09', 'M'),
('Patricia Pérez', '10360', 19, 2, 'B', '12345678-9', '2B10', 'F'),
('José Pérez', '10361', 18, 2, 'B', '12345678-9', '2B11', 'M'),
('Raquel Pérez', '10362', 19, 2, 'B', '12345678-9', '2B12', 'F'),
('Carlos Martínez', '10363', 18, 2, 'B', '12345678-9', '2B13', 'M'),
('Verónica Sánchez', '10364', 19, 2, 'B', '12345678-9', '2B14', 'F'),
('David Rodríguez', '10365', 18, 2, 'B', '12345678-9', '2B15', 'M'),
('Lucía Pérez', '10366', 19, 2, 'B', '12345678-9', '2B16', 'F'),
('José González', '10367', 18, 2, 'B', '12345678-9', '2B17', 'M'),
('Patricia González', '10368', 19, 2, 'B', '12345678-9', '2B18', 'F'),
('Carlos Pérez', '10369', 18, 2, 'B', '12345678-9', '2B19', 'M'),
('Raquel Martínez', '10370', 19, 2, 'B', '12345678-9', '2B20', 'F'),
('David González', '10371', 18, 2, 'B', '12345678-9', '2B21', 'M'),
('Marta Sánchez', '10372', 19, 2, 'B', '12345678-9', '2B22', 'F'),
('Tomás Pérez', '10373', 18, 2, 'B', '12345678-9', '2B23', 'M'),
('Cristina Rodríguez', '10374', 19, 2, 'B', '12345678-9', '2B24', 'F'),
('José Rodríguez', '10375', 18, 2, 'B', '12345678-9', '2B25', 'M'),
('Verónica López', '10376', 19, 2, 'B', '12345678-9', '2B26', 'F'),
('David Pérez', '10377', 18, 2, 'B', '12345678-9', '2B27', 'M'),
('Lucía Martínez', '10378', 19, 2, 'B', '12345678-9', '2B28', 'F'),
('Carlos Sánchez', '10379', 18, 2, 'B', '12345678-9', '2B29', 'M'),
('Raquel Pérez', '10380', 19, 2, 'B', '12345678-9', '2B30', 'F');

-- Sección 2C (General)
INSERT INTO estudiantes (nombre, nie, edad, año, seccion, dui, codigo, genero) VALUES
('Juan Pérez', '10381', 18, 2, 'C', '12345678-9', '2C01', 'M'),
('Marta Sánchez', '10382', 19, 2, 'C', '12345678-9', '2C02', 'F'),
('Carlos González', '10383', 18, 2, 'C', '12345678-9', '2C03', 'M'),
('Raquel Pérez', '10384', 19, 2, 'C', '12345678-9', '2C04', 'F'),
('José Rodríguez', '10385', 18, 2, 'C', '12345678-9', '2C05', 'M'),
('Lucía López', '10386', 19, 2, 'C', '12345678-9', '2C06', 'F'),
('David Martínez', '10387', 18, 2, 'C', '12345678-9', '2C07', 'M'),
('Cristina Sánchez', '10388', 19, 2, 'C', '12345678-9', '2C08', 'F'),
('Tomás González', '10389', 18, 2, 'C', '12345678-9', '2C09', 'M'),
('Patricia Rodríguez', '10390', 19, 2, 'C', '12345678-9', '2C10', 'F'),
('José Pérez', '10391', 18, 2, 'C', '12345678-9', '2C11', 'M'),
('Raquel González', '10392', 19, 2, 'C', '12345678-9', '2C12', 'F'),
('Carlos López', '10393', 18, 2, 'C', '12345678-9', '2C13', 'M'),
('Verónica Sánchez', '10394', 19, 2, 'C', '12345678-9', '2C14', 'F'),
('David Pérez', '10395', 18, 2, 'C', '12345678-9', '2C15', 'M'),
('Lucía Rodríguez', '10396', 19, 2, 'C', '12345678-9', '2C16', 'F'),
('José Martínez', '10397', 18, 2, 'C', '12345678-9', '2C17', 'M'),
('Patricia Pérez', '10398', 19, 2, 'C', '12345678-9', '2C18', 'F'),
('Carlos Rodríguez', '10399', 18, 2, 'C', '12345678-9', '2C19', 'M'),
('Raquel Martínez', '10400', 19, 2, 'C', '12345678-9', '2C20', 'F'),
('David González', '10401', 18, 2, 'C', '12345678-9', '2C21', 'M'),
('Marta López', '10402', 19, 2, 'C', '12345678-9', '2C22', 'F'),
('Tomás Pérez', '10403', 18, 2, 'C', '12345678-9', '2C23', 'M'),
('Cristina Pérez', '10404', 19, 2, 'C', '12345678-9', '2C24', 'F'),
('José Sánchez', '10405', 18, 2, 'C', '12345678-9', '2C25', 'M'),
('Verónica Pérez', '10406', 19, 2, 'C', '12345678-9', '2C26', 'F'),
('David Rodríguez', '10407', 18, 2, 'C', '12345678-9', '2C27', 'M'),
('Patricia González', '10408', 19, 2, 'C', '12345678-9', '2C28', 'F'),
('Carlos Pérez', '10409', 18, 2, 'C', '12345678-9', '2C29', 'M'),
('Raquel Sánchez', '10410', 19, 2, 'C', '12345678-9', '2C30', 'F');


-- Sección 2D (General)
INSERT INTO estudiantes (nombre, nie, edad, año, seccion, dui, codigo, genero) VALUES
('Juan Martínez', '10411', 18, 2, 'D', '12345678-9', '2D01', 'M'),
('Marta Rodríguez', '10412', 19, 2, 'D', '12345678-9', '2D02', 'F'),
('Carlos Sánchez', '10413', 18, 2, 'D', '12345678-9', '2D03', 'M'),
('Raquel Pérez', '10414', 19, 2, 'D', '12345678-9', '2D04', 'F'),
('José González', '10415', 18, 2, 'D', '12345678-9', '2D05', 'M'),
('Lucía López', '10416', 19, 2, 'D', '12345678-9', '2D06', 'F'),
('David Rodríguez', '10417', 18, 2, 'D', '12345678-9', '2D07', 'M'),
('Cristina Pérez', '10418', 19, 2, 'D', '12345678-9', '2D08', 'F'),
('Tomás Sánchez', '10419', 18, 2, 'D', '12345678-9', '2D09', 'M'),
('Patricia Martínez', '10420', 19, 2, 'D', '12345678-9', '2D10', 'F'),
('José Rodríguez', '10421', 18, 2, 'D', '12345678-9', '2D11', 'M'),
('Raquel López', '10422', 19, 2, 'D', '12345678-9', '2D12', 'F'),
('Carlos Pérez', '10423', 18, 2, 'D', '12345678-9', '2D13', 'M'),
('Verónica González', '10424', 19, 2, 'D', '12345678-9', '2D14', 'F'),
('David Martínez', '10425', 18, 2, 'D', '12345678-9', '2D15', 'M'),
('Lucía Sánchez', '10426', 19, 2, 'D', '12345678-9', '2D16', 'F'),
('José Pérez', '10427', 18, 2, 'D', '12345678-9', '2D17', 'M'),
('Patricia Rodríguez', '10428', 19, 2, 'D', '12345678-9', '2D18', 'F'),
('Carlos González', '10429', 18, 2, 'D', '12345678-9', '2D19', 'M'),
('Raquel Sánchez', '10430', 19, 2, 'D', '12345678-9', '2D20', 'F'),
('David Pérez', '10431', 18, 2, 'D', '12345678-9', '2D21', 'M'),
('Marta Martínez', '10432', 19, 2, 'D', '12345678-9', '2D22', 'F'),
('Tomás Rodríguez', '10433', 18, 2, 'D', '12345678-9', '2D23', 'M'),
('Cristina Sánchez', '10434', 19, 2, 'D', '12345678-9', '2D24', 'F'),
('José González', '10435', 18, 2, 'D', '12345678-9', '2D25', 'M'),
('Verónica López', '10436', 19, 2, 'D', '12345678-9', '2D26', 'F'),
('David Rodríguez', '10437', 18, 2, 'D', '12345678-9', '2D27', 'M'),
('Lucía Pérez', '10438', 19, 2, 'D', '12345678-9', '2D28', 'F'),
('Carlos Sánchez', '10439', 18, 2, 'D', '12345678-9', '2D29', 'M'),
('Raquel Pérez', '10440', 19, 2, 'D', '12345678-9', '2D30', 'F');

-- Sección 2E (General)
INSERT INTO estudiantes (nombre, nie, edad, año, seccion, dui, codigo, genero) VALUES
('Juan Pérez', '10441', 18, 2, 'E', '12345678-9', '2E01', 'M'),
('Marta Sánchez', '10442', 19, 2, 'E', '12345678-9', '2E02', 'F'),
('Carlos González', '10443', 18, 2, 'E', '12345678-9', '2E03', 'M'),
('Raquel Pérez', '10444', 19, 2, 'E', '12345678-9', '2E04', 'F'),
('José Rodríguez', '10445', 18, 2, 'E', '12345678-9', '2E05', 'M'),
('Lucía López', '10446', 19, 2, 'E', '12345678-9', '2E06', 'F'),
('David Martínez', '10447', 18, 2, 'E', '12345678-9', '2E07', 'M'),
('Cristina Sánchez', '10448', 19, 2, 'E', '12345678-9', '2E08', 'F'),
('Tomás González', '10449', 18, 2, 'E', '12345678-9', '2E09', 'M'),
('Patricia Rodríguez', '10450', 19, 2, 'E', '12345678-9', '2E10', 'F'),
('José Pérez', '10451', 18, 2, 'E', '12345678-9', '2E11', 'M'),
('Raquel González', '10452', 19, 2, 'E', '12345678-9', '2E12', 'F'),
('Carlos López', '10453', 18, 2, 'E', '12345678-9', '2E13', 'M'),
('Verónica Sánchez', '10454', 19, 2, 'E', '12345678-9', '2E14', 'F'),
('David Pérez', '10455', 18, 2, 'E', '12345678-9', '2E15', 'M'),
('Lucía Rodríguez', '10456', 19, 2, 'E', '12345678-9', '2E16', 'F'),
('José Martínez', '10457', 18, 2, 'E', '12345678-9', '2E17', 'M'),
('Patricia Pérez', '10458', 19, 2, 'E', '12345678-9', '2E18', 'F'),
('Carlos Rodríguez', '10459', 18, 2, 'E', '12345678-9', '2E19', 'M'),
('Raquel Martínez', '10460', 19, 2, 'E', '12345678-9', '2E20', 'F'),
('David González', '10461', 18, 2, 'E', '12345678-9', '2E21', 'M'),
('Marta López', '10462', 19, 2, 'E', '12345678-9', '2E22', 'F'),
('Tomás Pérez', '10463', 18, 2, 'E', '12345678-9', '2E23', 'M'),
('Cristina Pérez', '10464', 19, 2, 'E', '12345678-9', '2E24', 'F'),
('José Sánchez', '10465', 18, 2, 'E', '12345678-9', '2E25', 'M'),
('Verónica Pérez', '10466', 19, 2, 'E', '12345678-9', '2E26', 'F'),
('David Rodríguez', '10467', 18, 2, 'E', '12345678-9', '2E27', 'M'),
('Patricia González', '10468', 19, 2, 'E', '12345678-9', '2E28', 'F'),
('Carlos Pérez', '10469', 18, 2, 'E', '12345678-9', '2E29', 'M'),
('Raquel Sánchez', '10470', 19, 2, 'E', '12345678-9', '2E30', 'F');


-- Sección 2D (General)
INSERT INTO estudiantes (nombre, nie, edad, año, seccion, dui, codigo, genero) VALUES
('Juan Martínez', '10411', 18, 2, 'D', '12345678-9', '2D01', 'M'),
('Marta Rodríguez', '10412', 19, 2, 'D', '12345678-9', '2D02', 'F'),
('Carlos Sánchez', '10413', 18, 2, 'D', '12345678-9', '2D03', 'M'),
('Raquel Pérez', '10414', 19, 2, 'D', '12345678-9', '2D04', 'F'),
('José González', '10415', 18, 2, 'D', '12345678-9', '2D05', 'M'),
('Lucía López', '10416', 19, 2, 'D', '12345678-9', '2D06', 'F'),
('David Rodríguez', '10417', 18, 2, 'D', '12345678-9', '2D07', 'M'),
('Cristina Pérez', '10418', 19, 2, 'D', '12345678-9', '2D08', 'F'),
('Tomás Sánchez', '10419', 18, 2, 'D', '12345678-9', '2D09', 'M'),
('Patricia Martínez', '10420', 19, 2, 'D', '12345678-9', '2D10', 'F'),
('José Rodríguez', '10421', 18, 2, 'D', '12345678-9', '2D11', 'M'),
('Raquel López', '10422', 19, 2, 'D', '12345678-9', '2D12', 'F'),
('Carlos Pérez', '10423', 18, 2, 'D', '12345678-9', '2D13', 'M'),
('Verónica González', '10424', 19, 2, 'D', '12345678-9', '2D14', 'F'),
('David Martínez', '10425', 18, 2, 'D', '12345678-9', '2D15', 'M'),
('Lucía Sánchez', '10426', 19, 2, 'D', '12345678-9', '2D16', 'F'),
('José Pérez', '10427', 18, 2, 'D', '12345678-9', '2D17', 'M'),
('Patricia Rodríguez', '10428', 19, 2, 'D', '12345678-9', '2D18', 'F'),
('Carlos González', '10429', 18, 2, 'D', '12345678-9', '2D19', 'M'),
('Raquel Sánchez', '10430', 19, 2, 'D', '12345678-9', '2D20', 'F'),
('David Pérez', '10431', 18, 2, 'D', '12345678-9', '2D21', 'M'),
('Marta Martínez', '10432', 19, 2, 'D', '12345678-9', '2D22', 'F'),
('Tomás Rodríguez', '10433', 18, 2, 'D', '12345678-9', '2D23', 'M'),
('Cristina Sánchez', '10434', 19, 2, 'D', '12345678-9', '2D24', 'F'),
('José González', '10435', 18, 2, 'D', '12345678-9', '2D25', 'M'),
('Verónica López', '10436', 19, 2, 'D', '12345678-9', '2D26', 'F'),
('David Rodríguez', '10437', 18, 2, 'D', '12345678-9', '2D27', 'M'),
('Lucía Pérez', '10438', 19, 2, 'D', '12345678-9', '2D28', 'F'),
('Carlos Sánchez', '10439', 18, 2, 'D', '12345678-9', '2D29', 'M'),
('Raquel Pérez', '10440', 19, 2, 'D', '12345678-9', '2D30', 'F');

-- Sección 2E (General)
INSERT INTO estudiantes (nombre, nie, edad, año, seccion, dui, codigo, genero) VALUES
('Juan Pérez', '10441', 18, 2, 'E', '12345678-9', '2E01', 'M'),
('Marta Sánchez', '10442', 19, 2, 'E', '12345678-9', '2E02', 'F'),
('Carlos González', '10443', 18, 2, 'E', '12345678-9', '2E03', 'M'),
('Raquel Pérez', '10444', 19, 2, 'E', '12345678-9', '2E04', 'F'),
('José Rodríguez', '10445', 18, 2, 'E', '12345678-9', '2E05', 'M'),
('Lucía López', '10446', 19, 2, 'E', '12345678-9', '2E06', 'F'),
('David Martínez', '10447', 18, 2, 'E', '12345678-9', '2E07', 'M'),
('Cristina Sánchez', '10448', 19, 2, 'E', '12345678-9', '2E08', 'F'),
('Tomás González', '10449', 18, 2, 'E', '12345678-9', '2E09', 'M'),
('Patricia Rodríguez', '10450', 19, 2, 'E', '12345678-9', '2E10', 'F'),
('José Pérez', '10451', 18, 2, 'E', '12345678-9', '2E11', 'M'),
('Raquel González', '10452', 19, 2, 'E', '12345678-9', '2E12', 'F'),
('Carlos López', '10453', 18, 2, 'E', '12345678-9', '2E13', 'M'),
('Verónica Sánchez', '10454', 19, 2, 'E', '12345678-9', '2E14', 'F'),
('David Pérez', '10455', 18, 2, 'E', '12345678-9', '2E15', 'M'),
('Lucía Rodríguez', '10456', 19, 2, 'E', '12345678-9', '2E16', 'F'),
('José Martínez', '10457', 18, 2, 'E', '12345678-9', '2E17', 'M'),
('Patricia Pérez', '10458', 19, 2, 'E', '12345678-9', '2E18', 'F'),
('Carlos Rodríguez', '10459', 18, 2, 'E', '12345678-9', '2E19', 'M'),
('Raquel Martínez', '10460', 19, 2, 'E', '12345678-9', '2E20', 'F'),
('David González', '10461', 18, 2, 'E', '12345678-9', '2E21', 'M'),
('Marta López', '10462', 19, 2, 'E', '12345678-9', '2E22', 'F'),
('Tomás Pérez', '10463', 18, 2, 'E', '12345678-9', '2E23', 'M'),
('Cristina Pérez', '10464', 19, 2, 'E', '12345678-9', '2E24', 'F'),
('José Sánchez', '10465', 18, 2, 'E', '12345678-9', '2E25', 'M'),
('Verónica Pérez', '10466', 19, 2, 'E', '12345678-9', '2E26', 'F'),
('David Rodríguez', '10467', 18, 2, 'E', '12345678-9', '2E27', 'M'),
('Patricia González', '10468', 19, 2, 'E', '12345678-9', '2E28', 'F'),
('Carlos Pérez', '10469', 18, 2, 'E', '12345678-9', '2E29', 'M'),
('Raquel Sánchez', '10470', 19, 2, 'E', '12345678-9', '2E30', 'F');


INSERT INTO estudiantes (nombre, nie, edad, año, seccion, dui, codigo, genero) VALUES
('Juan Pérez', '10471', 18, 2, 'F', '12345678-9', '2F01', 'M'),
('Marta Sánchez', '10472', 19, 2, 'F', '12345678-9', '2F02', 'F'),
('Carlos González', '10473', 18, 2, 'F', '12345678-9', '2F03', 'M'),
('Raquel Pérez', '10474', 19, 2, 'F', '12345678-9', '2F04', 'F'),
('José Rodríguez', '10475', 18, 2, 'F', '12345678-9', '2F05', 'M'),
('Lucía López', '10476', 19, 2, 'F', '12345678-9', '2F06', 'F'),
('David Martínez', '10477', 18, 2, 'F', '12345678-9', '2F07', 'M'),
('Cristina Sánchez', '10478', 19, 2, 'F', '12345678-9', '2F08', 'F'),
('Tomás González', '10479', 18, 2, 'F', '12345678-9', '2F09', 'M'),
('Patricia Rodríguez', '10480', 19, 2, 'F', '12345678-9', '2F10', 'F'),
('José Pérez', '10481', 18, 2, 'F', '12345678-9', '2F11', 'M'),
('Raquel González', '10482', 19, 2, 'F', '12345678-9', '2F12', 'F'),
('Carlos López', '10483', 18, 2, 'F', '12345678-9', '2F13', 'M'),
('Verónica Sánchez', '10484', 19, 2, 'F', '12345678-9', '2F14', 'F'),
('David Pérez', '10485', 18, 2, 'F', '12345678-9', '2F15', 'M'),
('Lucía Rodríguez', '10486', 19, 2, 'F', '12345678-9', '2F16', 'F'),
('José Martínez', '10487', 18, 2, 'F', '12345678-9', '2F17', 'M'),
('Patricia Pérez', '10488', 19, 2, 'F', '12345678-9', '2F18', 'F'),
('Carlos Rodríguez', '10489', 18, 2, 'F', '12345678-9', '2F19', 'M'),
('Raquel Martínez', '10490', 19, 2, 'F', '12345678-9', '2F20', 'F'),
('David González', '10491', 18, 2, 'F', '12345678-9', '2F21', 'M'),
('Marta López', '10492', 19, 2, 'F', '12345678-9', '2F22', 'F'),
('Tomás Pérez', '10493', 18, 2, 'F', '12345678-9', '2F23', 'M'),
('Cristina Pérez', '10494', 19, 2, 'F', '12345678-9', '2F24', 'F'),
('José Sánchez', '10495', 18, 2, 'F', '12345678-9', '2F25', 'M'),
('Verónica Pérez', '10496', 19, 2, 'F', '12345678-9', '2F26', 'F'),
('David Rodríguez', '10497', 18, 2, 'F', '12345678-9', '2F27', 'M'),
('Patricia González', '10498', 19, 2, 'F', '12345678-9', '2F28', 'F'),
('Carlos Pérez', '10499', 18, 2, 'F', '12345678-9', '2F29', 'M'),
('Raquel Sánchez', '10500', 19, 2, 'F', '12345678-9', '2F30', 'F');

-- Sección 2G (General)
INSERT INTO estudiantes (nombre, nie, edad, año, seccion, dui, codigo, genero) VALUES
('Juan Pérez', '10501', 18, 2, 'G', '12345678-9', '2G01', 'M'),
('Marta Sánchez', '10502', 19, 2, 'G', '12345678-9', '2G02', 'F'),
('Carlos González', '10503', 18, 2, 'G', '12345678-9', '2G03', 'M'),
('Raquel Pérez', '10504', 19, 2, 'G', '12345678-9', '2G04', 'F'),
('José Rodríguez', '10505', 18, 2, 'G', '12345678-9', '2G05', 'M'),
('Lucía López', '10506', 19, 2, 'G', '12345678-9', '2G06', 'F'),
('David Martínez', '10507', 18, 2, 'G', '12345678-9', '2G07', 'M'),
('Cristina Sánchez', '10508', 19, 2, 'G', '12345678-9', '2G08', 'F'),
('Tomás González', '10509', 18, 2, 'G', '12345678-9', '2G09', 'M'),
('Patricia Rodríguez', '10510', 19, 2, 'G', '12345678-9', '2G10', 'F'),
('José Pérez', '10511', 18, 2, 'G', '12345678-9', '2G11', 'M'),
('Raquel González', '10512', 19, 2, 'G', '12345678-9', '2G12', 'F'),
('Carlos López', '10513', 18, 2, 'G', '12345678-9', '2G13', 'M'),
('Verónica Sánchez', '10514', 19, 2, 'G', '12345678-9', '2G14', 'F'),
('David Pérez', '10515', 18, 2, 'G', '12345678-9', '2G15', 'M'),
('Lucía Rodríguez', '10516', 19, 2, 'G', '12345678-9', '2G16', 'F'),
('José Martínez', '10517', 18, 2, 'G', '12345678-9', '2G17', 'M'),
('Patricia Pérez', '10518', 19, 2, 'G', '12345678-9', '2G18', 'F'),
('Carlos Rodríguez', '10519', 18, 2, 'G', '12345678-9', '2G19', 'M'),
('Raquel Martínez', '10520', 19, 2, 'G', '12345678-9', '2G20', 'F'),
('David González', '10521', 18, 2, 'G', '12345678-9', '2G21', 'M'),
('Marta López', '10522', 19, 2, 'G', '12345678-9', '2G22', 'F'),
('Tomás Pérez', '10523', 18, 2, 'G', '12345678-9', '2G23', 'M'),
('Cristina Pérez', '10524', 19, 2, 'G', '12345678-9', '2G24', 'F'),
('José Sánchez', '10525', 18, 2, 'G', '12345678-9', '2G25', 'M'),
('Verónica Pérez', '10526', 19, 2, 'G', '12345678-9', '2G26', 'F'),
('David Rodríguez', '10527', 18, 2, 'G', '12345678-9', '2G27', 'M'),
('Patricia González', '10528', 19, 2, 'G', '12345678-9', '2G28', 'F'),
('Carlos Pérez', '10529', 18, 2, 'G', '12345678-9', '2G29', 'M'),
('Raquel Sánchez', '10530', 19, 2, 'G', '12345678-9', '2G30', 'F');

INSERT INTO estudiantes (nombre, nie, edad, año, seccion, dui, codigo, genero) VALUES
('Juan Pérez', '10531', 18, 2, 'H', '12345678-9', '2H01', 'M'),
('Marta Sánchez', '10532', 19, 2, 'H', '12345678-9', '2H02', 'F'),
('Carlos González', '10533', 18, 2, 'H', '12345678-9', '2H03', 'M'),
('Raquel Pérez', '10534', 19, 2, 'H', '12345678-9', '2H04', 'F'),
('José Rodríguez', '10535', 18, 2, 'H', '12345678-9', '2H05', 'M'),
('Lucía López', '10536', 19, 2, 'H', '12345678-9', '2H06', 'F'),
('David Martínez', '10537', 18, 2, 'H', '12345678-9', '2H07', 'M'),
('Cristina Sánchez', '10538', 19, 2, 'H', '12345678-9', '2H08', 'F'),
('Tomás González', '10539', 18, 2, 'H', '12345678-9', '2H09', 'M'),
('Patricia Rodríguez', '10540', 19, 2, 'H', '12345678-9', '2H10', 'F'),
('José Pérez', '10541', 18, 2, 'H', '12345678-9', '2H11', 'M'),
('Raquel González', '10542', 19, 2, 'H', '12345678-9', '2H12', 'F'),
('Carlos López', '10543', 18, 2, 'H', '12345678-9', '2H13', 'M'),
('Verónica Sánchez', '10544', 19, 2, 'H', '12345678-9', '2H14', 'F'),
('David Pérez', '10545', 18, 2, 'H', '12345678-9', '2H15', 'M'),
('Lucía Rodríguez', '10546', 19, 2, 'H', '12345678-9', '2H16', 'F'),
('José Martínez', '10547', 18, 2, 'H', '12345678-9', '2H17', 'M'),
('Patricia Pérez', '10548', 19, 2, 'H', '12345678-9', '2H18', 'F'),
('Carlos Rodríguez', '10549', 18, 2, 'H', '12345678-9', '2H19', 'M'),
('Raquel Martínez', '10550', 19, 2, 'H', '12345678-9', '2H20', 'F'),
('David González', '10551', 18, 2, 'H', '12345678-9', '2H21', 'M'),
('Marta López', '10552', 19, 2, 'H', '12345678-9', '2H22', 'F'),
('Tomás Pérez', '10553', 18, 2, 'H', '12345678-9', '2H23', 'M'),
('Cristina Pérez', '10554', 19, 2, 'H', '12345678-9', '2H24', 'F'),
('José Sánchez', '10555', 18, 2, 'H', '12345678-9', '2H25', 'M'),
('Verónica Pérez', '10556', 19, 2, 'H', '12345678-9', '2H26', 'F'),
('David Rodríguez', '10557', 18, 2, 'H', '12345678-9', '2H27', 'M'),
('Patricia González', '10558', 19, 2, 'H', '12345678-9', '2H28', 'F'),
('Carlos Pérez', '10559', 18, 2, 'H', '12345678-9', '2H29', 'M'),
('Raquel Sánchez', '10560', 19, 2, 'H', '12345678-9', '2H30', 'F');

-- Sección 2I (General)
INSERT INTO estudiantes (nombre, nie, edad, año, seccion, dui, codigo, genero) VALUES
('Juan Pérez', '10561', 18, 2, 'I', '12345678-9', '2I01', 'M'),
('Marta Sánchez', '10562', 19, 2, 'I', '12345678-9', '2I02', 'F'),
('Carlos González', '10563', 18, 2, 'I', '12345678-9', '2I03', 'M'),
('Raquel Pérez', '10564', 19, 2, 'I', '12345678-9', '2I04', 'F'),
('José Rodríguez', '10565', 18, 2, 'I', '12345678-9', '2I05', 'M'),
('Lucía López', '10566', 19, 2, 'I', '12345678-9', '2I06', 'F'),
('David Martínez', '10567', 18, 2, 'I', '12345678-9', '2I07', 'M'),
('Cristina Sánchez', '10568', 19, 2, 'I', '12345678-9', '2I08', 'F'),
('Tomás González', '10569', 18, 2, 'I', '12345678-9', '2I09', 'M'),
('Patricia Rodríguez', '10570', 19, 2, 'I', '12345678-9', '2I10', 'F'),
('José Pérez', '10571', 18, 2, 'I', '12345678-9', '2I11', 'M'),
('Raquel González', '10572', 19, 2, 'I', '12345678-9', '2I12', 'F'),
('Carlos López', '10573', 18, 2, 'I', '12345678-9', '2I13', 'M'),
('Verónica Sánchez', '10574', 19, 2, 'I', '12345678-9', '2I14', 'F'),
('David Pérez', '10575', 18, 2, 'I', '12345678-9', '2I15', 'M'),
('Lucía Rodríguez', '10576', 19, 2, 'I', '12345678-9', '2I16', 'F'),
('José Martínez', '10577', 18, 2, 'I', '12345678-9', '2I17', 'M'),
('Patricia Pérez', '10578', 19, 2, 'I', '12345678-9', '2I18', 'F'),
('Carlos Rodríguez', '10579', 18, 2, 'I', '12345678-9', '2I19', 'M'),
('Raquel Martínez', '10580', 19, 2, 'I', '12345678-9', '2I20', 'F'),
('David González', '10581', 18, 2, 'I', '12345678-9', '2I21', 'M'),
('Marta López', '10582', 19, 2, 'I', '12345678-9', '2I22', 'F'),
('Tomás Pérez', '10583', 18, 2, 'I', '12345678-9', '2I23', 'M'),
('Cristina Pérez', '10584', 19, 2, 'I', '12345678-9', '2I24', 'F'),
('José Sánchez', '10585', 18, 2, 'I', '12345678-9', '2I25', 'M'),
('Verónica Pérez', '10586', 19, 2, 'I', '12345678-9', '2I26', 'F'),
('David Rodríguez', '10587', 18, 2, 'I', '12345678-9', '2I27', 'M'),
('Patricia González', '10588', 19, 2, 'I', '12345678-9', '2I28', 'F'),
('Carlos Pérez', '10589', 18, 2, 'I', '12345678-9', '2I29', 'M'),
('Raquel Sánchez', '10590', 19, 2, 'I', '12345678-9', '2I30', 'F');

INSERT INTO estudiantes (nombre, nie, edad, año, seccion, dui, codigo, genero) VALUES
('Juan Pérez', '10591', 18, 2, 'J', '12345678-9', '2J01', 'M'),
('Marta Sánchez', '10592', 19, 2, 'J', '12345678-9', '2J02', 'F'),
('Carlos González', '10593', 18, 2, 'J', '12345678-9', '2J03', 'M'),
('Raquel Pérez', '10594', 19, 2, 'J', '12345678-9', '2J04', 'F'),
('José Rodríguez', '10595', 18, 2, 'J', '12345678-9', '2J05', 'M'),
('Lucía López', '10596', 19, 2, 'J', '12345678-9', '2J06', 'F'),
('David Martínez', '10597', 18, 2, 'J', '12345678-9', '2J07', 'M'),
('Cristina Sánchez', '10598', 19, 2, 'J', '12345678-9', '2J08', 'F'),
('Tomás González', '10599', 18, 2, 'J', '12345678-9', '2J09', 'M'),
('Patricia Rodríguez', '10600', 19, 2, 'J', '12345678-9', '2J10', 'F'),
('José Pérez', '10601', 18, 2, 'J', '12345678-9', '2J11', 'M'),
('Raquel González', '10602', 19, 2, 'J', '12345678-9', '2J12', 'F'),
('Carlos López', '10603', 18, 2, 'J', '12345678-9', '2J13', 'M'),
('Verónica Sánchez', '10604', 19, 2, 'J', '12345678-9', '2J14', 'F'),
('David Pérez', '10605', 18, 2, 'J', '12345678-9', '2J15', 'M'),
('Lucía Rodríguez', '10606', 19, 2, 'J', '12345678-9', '2J16', 'F'),
('José Martínez', '10607', 18, 2, 'J', '12345678-9', '2J17', 'M'),
('Patricia Pérez', '10608', 19, 2, 'J', '12345678-9', '2J18', 'F'),
('Carlos Rodríguez', '10609', 18, 2, 'J', '12345678-9', '2J19', 'M'),
('Raquel Martínez', '10610', 19, 2, 'J', '12345678-9', '2J20', 'F'),
('David González', '10611', 18, 2, 'J', '12345678-9', '2J21', 'M'),
('Marta López', '10612', 19, 2, 'J', '12345678-9', '2J22', 'F'),
('Tomás Pérez', '10613', 18, 2, 'J', '12345678-9', '2J23', 'M'),
('Cristina Pérez', '10614', 19, 2, 'J', '12345678-9', '2J24', 'F'),
('José Sánchez', '10615', 18, 2, 'J', '12345678-9', '2J25', 'M'),
('Verónica Pérez', '10616', 19, 2, 'J', '12345678-9', '2J26', 'F'),
('David Rodríguez', '10617', 18, 2, 'J', '12345678-9', '2J27', 'M'),
('Patricia González', '10618', 19, 2, 'J', '12345678-9', '2J28', 'F'),
('Carlos Pérez', '10619', 18, 2, 'J', '12345678-9', '2J29', 'M'),
('Raquel Sánchez', '10620', 19, 2, 'J', '12345678-9', '2J30', 'F');

-- Sección 2K (General)
INSERT INTO estudiantes (nombre, nie, edad, año, seccion, dui, codigo, genero) VALUES
('Juan Pérez', '10621', 18, 2, 'K', '12345678-9', '2K01', 'M'),
('Marta Sánchez', '10622', 19, 2, 'K', '12345678-9', '2K02', 'F'),
('Carlos González', '10623', 18, 2, 'K', '12345678-9', '2K03', 'M'),
('Raquel Pérez', '10624', 19, 2, 'K', '12345678-9', '2K04', 'F'),
('José Rodríguez', '10625', 18, 2, 'K', '12345678-9', '2K05', 'M'),
('Lucía López', '10626', 19, 2, 'K', '12345678-9', '2K06', 'F'),
('David Martínez', '10627', 18, 2, 'K', '12345678-9', '2K07', 'M'),
('Cristina Sánchez', '10628', 19, 2, 'K', '12345678-9', '2K08', 'F'),
('Tomás González', '10629', 18, 2, 'K', '12345678-9', '2K09', 'M'),
('Patricia Rodríguez', '10630', 19, 2, 'K', '12345678-9', '2K10', 'F'),
('José Pérez', '10631', 18, 2, 'K', '12345678-9', '2K11', 'M'),
('Raquel González', '10632', 19, 2, 'K', '12345678-9', '2K12', 'F'),
('Carlos López', '10633', 18, 2, 'K', '12345678-9', '2K13', 'M'),
('Verónica Sánchez', '10634', 19, 2, 'K', '12345678-9', '2K14', 'F'),
('David Pérez', '10635', 18, 2, 'K', '12345678-9', '2K15', 'M'),
('Lucía Rodríguez', '10636', 19, 2, 'K', '12345678-9', '2K16', 'F'),
('José Martínez', '10637', 18, 2, 'K', '12345678-9', '2K17', 'M'),
('Patricia Pérez', '10638', 19, 2, 'K', '12345678-9', '2K18', 'F'),
('Carlos Rodríguez', '10639', 18, 2, 'K', '12345678-9', '2K19', 'M'),
('Raquel Martínez', '10640', 19, 2, 'K', '12345678-9', '2K20', 'F'),
('David González', '10641', 18, 2, 'K', '12345678-9', '2K21', 'M'),
('Marta López', '10642', 19, 2, 'K', '12345678-9', '2K22', 'F'),
('Tomás Pérez', '10643', 18, 2, 'K', '12345678-9', '2K23', 'M'),
('Cristina Pérez', '10644', 19, 2, 'K', '12345678-9', '2K24', 'F'),
('José Sánchez', '10645', 18, 2, 'K', '12345678-9', '2K25', 'M'),
('Verónica Pérez', '10646', 19, 2, 'K', '12345678-9', '2K26', 'F'),
('David Rodríguez', '10647', 18, 2, 'K', '12345678-9', '2K27', 'M'),
('Patricia González', '10648', 19, 2, 'K', '12345678-9', '2K28', 'F'),
('Carlos Pérez', '10649', 18, 2, 'K', '12345678-9', '2K29', 'M'),
('Raquel Sánchez', '10650', 19, 2, 'K', '12345678-9', '2K30', 'F');

INSERT INTO padres (nombre, numero , correo ,dui) VALUES ('juanpaco', '64222002', 'Juanpaco@gmail.com' ,'12345678-9');


TRUNCATE TABLE salida;

