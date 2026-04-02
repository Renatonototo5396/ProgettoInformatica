# SISTEMA DI GESTIONE DELLE SPESE PERSONALI
# File: main.py

import sqlite3
import os
import re

NOME_DB = "spese_personali.db"

def connetti_db():
    conn = sqlite3.connect(NOME_DB)
    conn.execute("PRAGMA foreign_keys = ON")
    crea_tabella(conn)
    return conn

def crea_tabella(conn):
    cursore = conn.cursor()
    cursore.executescript("""
      CREATE TABLE IF NOT EXISTS Categorie (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Nome TEXT NOT NULL UNIQUE 
    );

    CREATE TABLE IF NOT EXISTS Spese (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Data TEXT NOT NULL,
        Importo REAL NOT NULLA CHECK (Importo > 0),
        Categoria_id INTEGER NOT NULL,
        Descreizione TEXT,
        FOREIGN KEY (Categoria_id) REFERENCES Categoria(ID)
            ON DELETE RESTRICT ON UPDATE CASCADE
    );
                          
    CREATE TABLE IF NOT EXISTS Budget_mensile (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Mese TEXT NOT NULL,
        Categoria_id INTEGER NOT NULL,
        Importo_budget REAL NOT NULL CHECK (Importo_budget > 0),
        UNIQUE (Mese, Categoria_id),
        FOREIGN KEY (Categoria_id) REFERENCES Categoria(ID)
        ON DELETE RESTRICT ON UPDATE CASCADE
        ); 
                          """)
    conn.commit()
    