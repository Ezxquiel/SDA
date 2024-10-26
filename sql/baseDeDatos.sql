CREATE TABLE Parents (
    Id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    FullName VARCHAR(60),
    phone int(10),                              -- Cambiado a VARCHAR para permitir caracteres como +
    Gmail VARCHAR(100),
    Dui VARCHAR(15) UNIQUE                          -- Cambiado a VARCHAR y añadido UNIQUE
);

CREATE TABLE Student (
    Id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    FullName VARCHAR(60),
    Nie VARCHAR(15),                                -- Cambiado a VARCHAR
    age INT CHECK (age >= 0),                       -- Asegurarse de que la edad sea no negativa
    section VARCHAR(1),
    year INT,                                       -- Validar el año
    code INT,                                       -- Considera qué longitud usar
    Dui VARCHAR(15),                                -- Cambiado a VARCHAR
    FOREIGN KEY (Dui) REFERENCES Parents(Dui)       -- Clave foránea
);
