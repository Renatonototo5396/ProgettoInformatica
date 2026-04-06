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

def crea_tabella(conn): # CREAZIONE TABELLE SQL
    cursore = conn.cursor()
    cursore.executescript("""
                          
      CREATE TABLE IF NOT EXISTS Categorie (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE 
    );

    CREATE TABLE IF NOT EXISTS Spese (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT NOT NULL,
        importo REAL NOT NULLA CHECK (importo > 0),
        categoria_id INTEGER NOT NULL,
        descreizione TEXT,
        FOREIGN KEY (categoria_id) REFERENCES categoria(ID)
        ON DELETE RESTRICT ON UPDATE CASCADE
    );
                          
    CREATE TABLE IF NOT EXISTS Budget_mensile (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Mese TEXT NOT NULL,
        Categoria_id INTEGER NOT NULL,
        importo_budget REAL NOT NULL CHECK (importo_budget > 0),
        UNIQUE (Mese, Categoria_id),
        FOREIGN KEY (Categoria_id) REFERENCES Categoria(ID)
        ON DELETE RESTRICT ON UPDATE CASCADE
        ); 
                          """)
    conn.commit()
    
def pulisci_schermo(): # PULISCE LO SCHERMO DA EVENTUALI ERRORI
        os.system("cls" if os.name == "nt" else "clear")

def stampa_separatore(lunghezza=40): # AGGIUNGE SEPARATORE - 40 VOLTE
            print ("-" * lunghezza)

def pausa():
    input("\nPremi INVIO per continuare...")

# MODULO 1 

def gestione_categorie(conn):
      pulisci_schermo()
      stampa_separatore()
      print("GESTIONE CATEGORIE")
      stampa_separatore()

      nome = input("Inserisci il nome della nuova categoria").strip()

      if not nome:
            print("\nErrore il nome non può essere vuoto.")
            pausa()
            return
      cursore = conn.cursor
      cursore.execute(
          "SELECT ID FROM Categorie WHERE LOWER(nome) =LOWER (?)", (nome)
     )
      if cursore.fetchone():
          print("\nErrore: la categoria '{nome}' esiste già.")
          pausa()
          return
      cursore.execute("INSERTO INTO Categorie (nome) VALUES (?)" , (nome,))
      print("\nCategoria '{nome}' inserita correttamente.")
      pausa()


# VALIDAZIONE FORMATO DATA 
def valida_data(data):
    parti = data.split("-")
    if len(parti) != 3:
        return False
    if len(parti[0]) != 4 or len(parti[1]) != 2 or len(parti[2]) != 2:
        return False
    if not parti[0].isdigit() or not parti[1].isdigit() or not parti[2].isdigit():
        return False
    return True

def inserisci_spesa(conn):
     pulisci_schermo()
     stampa_separatore()
     print("INSERISCI SPESA")
     stampa_separatore()

     # INPUT INSERIMENTO DATA 
     data = input("Data (formato YYYY-MM-DD: )").strip()
     if not valida_data(data):
          print("\nErrore: formato data non valido. Usa YYY-MM-DD")
          pausa
          return
     # INPUT INSERIMENTO IMPORTO
     try:
        importo =float(input("Importo: "))
     except ValueError:
          print("\nErrore: inserisci un numero valido.")
          pausa()
          return
     if importo <=0:
          print("\nErrore: l'importo deve essere maggiore di zero.")
          pausa()         
          return
     # INPUT INSERIMENTO CATEGORIA 
     categoria_nome = input ("Categoria: ").strip()
     if not categoria_nome:
          print("\nErrore: il campo non può essere vuoto.")
          pausa()
          return
     cursore = conn.cursor()
     cursore.execute(
          "SELECT ID FROM Categorie WHERE LOWER(nome) = LOWER(?)", (categoria_nome)
     )
     riga = cursore.fetchone()
     if not riga:
          print("\nErrore: la categoria '{categoria_nome}' non esiste.")
          pausa()
          return
     categoria_id = riga[0]

     # INSERIMENTO DESCRIZIONE (OPZIONALE)
     descrizione = input("Descrizione (premi INVIO per saltare)").strip()
     if not descrizione:
          descrizione=None
    
     cursore.execute(
          "INSERT INTO spese (data, improto, categoria_id, descrizione) VALUES (?,?,?,?,?)",
          (data, importo, categoria_id, descrizione)
         
    )
     conn.commit()
     print("\nSpesa inserita correttamente.")
     pausa()
     