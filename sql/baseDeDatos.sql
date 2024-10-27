CREATE TABLE padres (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(60),
    numero VARCHAR(15),  									-- Permitir caracteres como +
    correo VARCHAR(100),
    dui VARCHAR(15) UNIQUE                                -- UNIQUE para que el DUI sea único
);

CREATE TABLE seccion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    seccion VARCHAR(1),
    year INT,
    especialidad VARCHAR(20)
);

CREATE TABLE estudiantes (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(60),
    nie VARCHAR(15) UNIQUE,                             -- Aseguramos que el NIE sea único
    edad TINYINT,                                       -- Cambiado INT(2) a TINYINT por eficiencia
    seccion_id INT,
    año INT,                                            -- Mantener el campo year
    codigo INT,
    dui VARCHAR(15),
    especialidad_id INT,
    FOREIGN KEY (seccion_id) REFERENCES seccion(id),
    FOREIGN KEY (año) REFERENCES seccion(year),
    FOREIGN KEY (especialidad_id) REFERENCES seccion(id),
    FOREIGN KEY (dui) REFERENCES padres(dui)
);

CREATE TABLE entrada (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nie VARCHAR(15),                                    -- Coincide con estudiantes
    data DATE,
    hour TIME,
    FOREIGN KEY (nie) REFERENCES estudiantes(nie)
);

CREATE TABLE salida (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nie VARCHAR(15),                                    -- Coincide con estudiantes
    data DATE,
    hour TIME,
    FOREIGN KEY (nie) REFERENCES estudiantes(nie)
);

SELECT * FROM padres
