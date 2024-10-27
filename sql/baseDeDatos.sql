CREATE DATABASE by8ekzvhusvvn2yqc71b;
USE by8ekzvhusvvn2yqc71b;

CREATE TABLE padres (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(60),
    numero VARCHAR(15) UNIQUE,   
    correo VARCHAR(100) UNIQUE,
    dui VARCHAR(15) UNIQUE        
);

CREATE TABLE seccion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    seccion VARCHAR(1),
    año INT,
    especialidad VARCHAR(20) UNIQUE  -- Ensure this has a UNIQUE constraint
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
);

CREATE TABLE salida (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nie VARCHAR(15),                                
    data DATE,
    hour TIME,
    FOREIGN KEY (nie) REFERENCES estudiantes(nie)
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