CREATE DATABASE by8ekzvhusvvn2yqc71b;
USE by8ekzvhusvvn2yqc71b;

CREATE TABLE padres (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(60),
    numero VARCHAR(15) UNIQUE,   
    correo VARCHAR(100) UNIQUE,
    dui VARCHAR(15) UNIQUE        
<<<<<<< HEAD
-- Crear la base de datos y seleccionarla
CREATE DATABASE pruebaFull1;
USE pruebaFull1;

-- Crear la tabla Parents
CREATE TABLE Parents (
    Id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    FullName VARCHAR(60),
    phone VARCHAR(15),                            
    Gmail VARCHAR(100),
    Dui VARCHAR(15) UNIQUE                         -- Definir Dui como único para la relación
=======
>>>>>>> 2288a5b2d1469c020bcdcb82a873c221c18b046e
);

CREATE TABLE seccion (
-- Crear la tabla section
CREATE TABLE section (
    id INT AUTO_INCREMENT PRIMARY KEY,
    seccion VARCHAR(1),
    año INT,
    especialidad VARCHAR(20) UNIQUE  -- Ensure this has a UNIQUE constraint
<<<<<<< HEAD
    section VARCHAR(1),
    year INT,
    specialty VARCHAR(20),
    UNIQUE (section, year, specialty)              -- Crear índice único para claves foráneas
=======
>>>>>>> 2288a5b2d1469c020bcdcb82a873c221c18b046e
);

CREATE TABLE estudiantes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(200),
    nie VARCHAR(15) UNIQUE,                             
    edad TINYINT,    
    año INT,
    codigo VARCHAR(4),
    seccion INT,
    FOREIGN KEY (seccion) REFERENCES seccion(id),
    dui VARCHAR(15),
    FOREIGN KEY (dui) REFERENCES padres(dui),
    especialidad VARCHAR(100),
    FOREIGN KEY (especialidad) REFERENCES seccion(especialidad)  -- Ensure this references a UNIQUE column
);

CREATE TABLE entrada (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nie VARCHAR(15),                                    
    data DATE,
    hour TIME,
    FOREIGN KEY (nie) REFERENCES estudiantes(nie)
-- Crear la tabla Student con claves foráneas hacia las tablas section y Parents
CREATE TABLE Student (
    Id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    FullName VARCHAR(60),
    Nie VARCHAR(15) UNIQUE,                        -- Definir Nie como único para la relación
    age INT CHECK (age >= 0),                    
    section VARCHAR(1),
    year INT,                                      
    code INT,
    Dui VARCHAR(15),   
    specialty VARCHAR(20),                      
    FOREIGN KEY (section, year, specialty) REFERENCES section(section, year, specialty),
    FOREIGN KEY (Dui) REFERENCES Parents(Dui)
);

CREATE TABLE salida (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nie VARCHAR(15),                                
<<<<<<< HEAD

-- Crear la tabla assists con clave foránea hacia la tabla Student
CREATE TABLE assists (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Nie VARCHAR(15),                             
=======
>>>>>>> 2288a5b2d1469c020bcdcb82a873c221c18b046e
    data DATE,
    hour TIME,
    FOREIGN KEY (nie) REFERENCES estudiantes(nie)
    FOREIGN KEY (Nie) REFERENCES Student(Nie)      -- Clave foránea para Nie
);

SELECT 
    e.*,
    p.nombre AS nombre_padre,
    p.numero AS telefono_padre,
    p.correo AS correo_padre
FROM 
    estudiantes e
LEFT JOIN 
    padres p ON e.dui = p.dui;



SELECT * FROM estudiantes