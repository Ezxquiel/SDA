CREATE TABLE Parents (
    Id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    FullName VARCHAR(60),
    phone VARCHAR(15),                            -- Cambiado a VARCHAR para permitir caracteres como +
    Gmail VARCHAR(100),
    Dui VARCHAR(15) UNIQUE                        -- Cambiado a VARCHAR y añadido UNIQUE
);

CREATE TABLE section (
    id INT AUTO_INCREMENT PRIMARY KEY,
    section VARCHAR(1),
    year INT,
    specialty VARCHAR(20)
);

CREATE TABLE Student (
    Id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    FullName VARCHAR(60),
    Nie VARCHAR(15),                              
    age INT(2),                    
    section VARCHAR(1),
    year INT,                                      
    code INT,
    Dui VARCHAR(15),   
    specialty VARCHAR(20),                      
    FOREIGN KEY (section) REFERENCES section(section),
    FOREIGN KEY (year) REFERENCES section(year),
    FOREIGN KEY (specialty) REFERENCES section(specialty),
    FOREIGN KEY (Dui) REFERENCES Parents(Dui)
);


CREATE TABLE assists (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Nie VARCHAR(15),                              -- Cambiado a VARCHAR para coincidir con Student
    data DATE,
    hour TIME,
    FOREIGN KEY (Nie) REFERENCES Student(Nie)
);
