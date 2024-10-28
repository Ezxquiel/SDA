
-- Primera tabla: padres
CREATE TABLE padres (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(60),
    numero VARCHAR(15) UNIQUE,
    correo VARCHAR(100) UNIQUE,
    dui VARCHAR(15) 
);

-- Segunda tabla: seccion (con los índices necesarios)
CREATE TABLE seccion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    seccion VARCHAR(1) NOT NULL,
    año INT NOT NULL,
    especialidad VARCHAR(20) NOT NULL,
    UNIQUE KEY unique_especialidad (especialidad),
    KEY idx_seccion (seccion),
    KEY idx_año (año)
);

-- Tercera tabla: estudiantes
CREATE TABLE estudiantes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(200) NOT NULL,
    nie VARCHAR(15) UNIQUE NOT NULL,
    edad TINYINT,
    año INT NOT NULL,
    seccion VARCHAR(1) NOT NULL,
    dui VARCHAR(15),
    especialidad VARCHAR(20),
    codigo VARCHAR(4),
    FOREIGN KEY (año) REFERENCES seccion(año),
    FOREIGN KEY (seccion) REFERENCES seccion(seccion),
    FOREIGN KEY (dui) REFERENCES padres(dui),
    FOREIGN KEY (especialidad) REFERENCES seccion(especialidad)
);

-- Cuarta tabla: entrada
CREATE TABLE entrada (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nie VARCHAR(15),
    fecha DATE,
    hora TIME,
    FOREIGN KEY (nie) REFERENCES estudiantes(nie)
);

-- Quinta tabla: salida
CREATE TABLE salida (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nie VARCHAR(15),
    fecha DATE,
    hora TIME,
    FOREIGN KEY (nie) REFERENCES estudiantes(nie)
);



SELECT 
    e.id AS estudiante_id,
    e.nombre AS nombre_estudiante,
    e.nie,
    e.edad,
    e.codigo,
    s.seccion,
    s.año,
    s.especialidad,
    p.nombre AS nombre_padre,
    p.numero AS numero_padre,
    p.correo AS correo_padre,
    p.dui AS dui_padre
FROM 
    estudiantes e
JOIN 
    seccion s ON e.año = s.año AND e.seccion = s.seccion  -- Join with seccion
LEFT JOIN 
    padres p ON e.dui = p.dui;  -- Left join with padres to get parent info