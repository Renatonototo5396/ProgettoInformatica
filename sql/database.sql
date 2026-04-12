-- Sistema di gestione spese personali
-- File: Database.sql
-- Database: MySql

CREATE DATABASE IF NOT EXISTS spese_personali;
USE spese_personali;


-----------------------------------
-- TABELLA: Categoria
-----------------------------------

CREATE TABLE IF NOT EXISTS Categorie (
    ID INTEGER PRIMARY KEY AUTO_INCREMENT,
    Nome VARCHAR(255) NOT NULL UNIQUE 
);

------------------------------------
-- TABELLA: Spese
------------------------------------

CREATE TABLE IF NOT EXISTS Spese (
    ID INTEGER PRIMARY KEY AUTO_INCREMENT,
    Data VARCHAR(255) NOT NULL,
    Importo REAL NOT NULL CHECK (Importo > 0),
    Categoria_id INTEGER NOT NULL,
    Descreizione VARCHAR(255),
    FOREIGN KEY (Categoria_id) REFERENCES Categoria(ID)
    ON DELETE RESTRICT  ON UPDATE CASCADE
);

------------------------------------
-- TABELLA: Budget_mensile
------------------------------------

CREATE TABLE IF NOT EXISTS Budget_mensile (
    ID INTEGER PRIMARY KEY AUTO_INCREMENT,
    Mese VARCHAR(255) NOT NULL,
    Categoria_id INTEGER NOT NULL,
    Importo_budget REAL NOT NULL CHECK (Importo_budget > 0),
    UNIQUE (Mese, Categoria_id),
    FOREIGN KEY (Categoria_id) REFERENCES Categoria(ID)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
);

------------------------------------
-- INSERIMENTO DATI ESEMPIO
------------------------------------
-- INSERIMENTO CATEGORIE

INSERT INTO Categoria (Nome) VALUES ("Alimentari");
INSERT INTO Categoria (Nome) VALUES ("Viaggi");
INSERT INTO Categoria (Nome) VALUES ("Svago");
INSERT INTO Categoria (Nome) VALUES ("Shopping");
INSERT INTO Categoria (Nome) VALUES ("Collezionabili");
INSERT INTO Categoria (Nome) VALUES ("Varie");

-- INSERIMENTO SPESE

INSERT INTO Spese (Data, Importo, Categoria_id, Descreizione)
VALUES ("2026-02-28", 52, 5, "Pokemon");
INSERT INTO Spese (Data, Importo, Categoria_id, Descreizione)
VALUES ("2026-01-12", 12, 1, "Uovo di Pasqua");
INSERT INTO Spese (Data, Importo, Categoria_id, Descreizione)
VALUES ("2025-11-01", 100, 2, "Diesel");
INSERT INTO Spese (Data, Importo, Categoria_id, Descreizione)
VALUES ("2026-01-22", 120, 4, "Zara");
INSERT INTO Spese (Data, Importo, Categoria_id, Descreizione)
VALUES ("2026-03-28", 103, 5, "Pokemon");
INSERT INTO Spese (Data, Importo, Categoria_id, Descreizione)
VALUES ("2026-03-22", 10, 6, "Cinema");
INSERT INTO Spese (Data, Importo, Categoria_id, Descreizione)
VALUES ("2026-01-11", 200, 2, "Viaggio Madrid");
INSERT INTO Spese (Data, Importo, Categoria_id, Descreizione)
VALUES ("2026-03-05", 250, 3, "Cena Stellata");

-- INSERIMENTO BUDGET MENSILE

INSERT INTO Budget_mensile (Mese, Categoria_id, Importo_budget)
VALUES ("2025-01", 1 , 200);
INSERT INTO Budget_mensile (Mese, Categoria_id, Importo_budget)
VALUES ("2025-01", 2 , 400);
INSERT INTO Budget_mensile (Mese, Categoria_id, Importo_budget)
VALUES ("2025-01", 3 , 300);
INSERT INTO Budget_mensile (Mese, Categoria_id, Importo_budget)
VALUES ("2025-01", 4 , 500);
INSERT INTO Budget_mensile (Mese, Categoria_id, Importo_budget)
VALUES ("2026-01", 5 , 500);
INSERT INTO Budget_mensile (Mese, Categoria_id, Importo_budget)
VALUES ("2026-01", 6 ,40);
