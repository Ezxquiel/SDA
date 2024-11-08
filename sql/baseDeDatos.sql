-- Create the database
CREATE DATABASE by8ekzvhusvvn2yqc71b;
USE by8ekzvhusvvn2yqc71b;

CREATE TABLE padres (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(60) NOT NULL,
    numero VARCHAR(15) UNIQUE NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL,
    dui VARCHAR(15) UNIQUE NOT NULL  -- Asegurar que el DUI sea único
);

CREATE TABLE seccion (
    año INT NOT NULL,
    seccion VARCHAR(1) NOT NULL,
    especialidad VARCHAR(20) NOT NULL,
    PRIMARY KEY (año, seccion),  -- Clave primaria compuesta
    UNIQUE KEY unique_especialidad (especialidad)  -- Asegurar que especialidad sea única
);

CREATE TABLE estudiantes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(200) NOT NULL,
    nie VARCHAR(15) UNIQUE NOT NULL,
    edad TINYINT,
    genero VARCHAR (1),
    año INT NOT NULL,
    seccion VARCHAR(1) NOT NULL,
    dui VARCHAR(15),
    especialidad VARCHAR(20),
    codigo VARCHAR(4),
    FOREIGN KEY (año, seccion) REFERENCES seccion(año, seccion),  -- Clave compuesta referenciada
    FOREIGN KEY (dui) REFERENCES padres(dui),
    FOREIGN KEY (especialidad) REFERENCES seccion(especialidad)  -- Referencia a especialidad
);

CREATE TABLE entrada (
    id_entrada INT PRIMARY KEY AUTO_INCREMENT,
    nie VARCHAR(15) NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    FOREIGN KEY (nie) REFERENCES estudiantes(nie)
);

CREATE TABLE salida (
    id_salida INT PRIMARY KEY AUTO_INCREMENT,
    nie VARCHAR(15) NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    FOREIGN KEY (nie) REFERENCES estudiantes(nie)
);

CREATE TABLE total (
	id_total INT PRIMARY KEY AUTO_INCREMENT
);