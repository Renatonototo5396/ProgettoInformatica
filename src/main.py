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
        importo REAL NOT NULL CHECK (importo > 0),
        categoria_id INTEGER NOT NULL,
        descrizione TEXT,
        FOREIGN KEY (categoria_id) REFERENCES categorie(ID)
        ON DELETE RESTRICT ON UPDATE CASCADE
    );
                          
    CREATE TABLE IF NOT EXISTS Budget_mensile (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Mese TEXT NOT NULL,
        Categoria_id INTEGER NOT NULL,
        importo_budget REAL NOT NULL CHECK (importo_budget > 0),
        UNIQUE (Mese, Categoria_id),
        FOREIGN KEY (Categoria_id) REFERENCES Categorie(ID)
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

    nome = input("Inserisci il nome della nuova categoria: ").strip()

    if not nome:
        print("\nErrore il nome non può essere vuoto.")
        pausa()
        return
    cursore = conn.cursor()
    cursore.execute(
        "SELECT ID FROM Categorie WHERE LOWER(nome) =LOWER (?)", (nome,)
    )
    if cursore.fetchone():
        print(f"\nErrore: la categoria '{nome}' esiste già.")
        pausa()
        return
    cursore.execute("INSERT INTO Categorie (nome) VALUES (?)" , (nome,))
    conn.commit()
    print(f"\nCategoria '{nome}' inserita correttamente.")
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
     
     data = input("Data (formato YYYY-MM-DD): ").strip()
     if not valida_data(data):
        print("\nErrore: formato data non valido. Usa YYYY-MM-DD")
        pausa()
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
          "SELECT ID FROM Categorie WHERE LOWER(nome) = LOWER(?)", (categoria_nome,)
     )
     riga = cursore.fetchone()
     if not riga:
        print(f"\nErrore: la categoria '{categoria_nome}' non esiste.")
        pausa()
        return
     categoria_id = riga[0]

     # INSERIMENTO DESCRIZIONE (OPZIONALE)
     
     descrizione = input("Descrizione (premi INVIO per saltare)").strip()
     if not descrizione:
          descrizione=None
    
     cursore.execute(
          "INSERT INTO Spese (data, importo, categoria_id, descrizione) VALUES (?,?,?,?)",
          (data, importo, categoria_id, descrizione)
         
    )
     conn.commit()
     print("\nSpesa inserita correttamente.")
     pausa()

def valida_mese(mese):
    parti = mese.split("-")
    if len(parti) != 2:
        return False
    if len(parti[0]) != 4 or len(parti[1]) != 2:
        return False
    if not parti[0].isdigit() or not parti[1].isdigit():
        return False
    return True


def definisci_budget(conn):
    pulisci_schermo()
    stampa_separatore()
    print("DEFINISCI BUDGET MENSILE")
    stampa_separatore()

    mese = input("Mese (formato YYYY-MM, es. 2025-01): ").strip()
    if not valida_mese(mese):
        print("\nErrore: formato mese non valido. Usa YYYY-MM.")
        pausa()
        return

    categoria_nome = input("Categoria: ").strip()
    if not categoria_nome:
        print("\nErrore: il nome della categoria non può essere vuoto.")
        pausa()
        return

    cursore = conn.cursor()
    cursore.execute(
        "SELECT ID FROM Categorie WHERE LOWER(nome) = LOWER(?)", (categoria_nome,)
    )
    riga = cursore.fetchone()
    if not riga:
        print(f"\nErrore: la categoria '{categoria_nome}' non esiste.")
        pausa()
        return

    categoria_id = riga[0]

    try:
        importo_budget = float(input("Importo budget: ").strip())
    except ValueError:
        print("\nErrore: inserisci un numero valido.")
        pausa()
        return

    if importo_budget <= 0:
        print("\nErrore: il budget deve essere maggiore di zero.")
        pausa()
        return

    cursore.execute("""
        INSERT INTO Budget_mensile (mese, Categoria_id, importo_budget)
        VALUES (?, ?, ?)
        ON CONFLICT(mese, Categoria_id) DO UPDATE SET importo_budget = excluded.importo_budget
    """, (mese, categoria_id, importo_budget))
    conn.commit()
    print("\nBudget mensile salvato correttamente.")
    pausa()

def visualizza_report(conn):
    while True:
        pulisci_schermo()
        stampa_separatore()
        print("REPORT")
        stampa_separatore()
        print (" 1. Totale spese per categoria")
        print (" 2. Spese mensili vs Budget")
        print (" 3. Elenco completo spese")
        print (" 4. Ritorna al menù principale")
        stampa_separatore()
        
        scelta = input(" Inserisci la tua scelta: ").strip()
        
        if scelta == "1":
            report_totale_categorie(conn)
        elif scelta == "2":
            report_spese_vs_budget(conn)
        elif scelta == "3":
            report_elenco_spese(conn)
        elif scelta == "4":
            break
        else:
            print ("\nScelta non valida. Riprova.")
            pausa()
            
def report_totale_categorie(conn):
    pulisci_schermo()
    stampa_separatore()          
    print (" REPORT 1 - TOTALE SPESE PER CATEGORIA")
    stampa_separatore()
    cursore = conn.cursor()
    cursore.execute("""
        SELECT c.nome, SUM(s.importo)
        FROM Spese s
        JOIN Categorie c On s.categoria_id = c.ID
        GROUP BY c.nome
        ORDER BY SUM(s.importo) DESC
        """)
    righe = cursore.fetchall()
    
    if not righe:
        print("\nNessuna spesa registrata.")
    else:
        print (f"\n{'Categoria': <20} {'Totale':>10}")
        stampa_separatore(32)
        for categoria, totale in righe:
            print (f"{categoria:<20} {totale:>9.2f} €")
        stampa_separatore(32)
        totale_generale= sum(r[1] for r in righe)
        print (f"{'TOTALE GENERALE':<20} {totale_generale:>9.2f} €")
    pausa()
                
def report_spese_vs_budget(conn):
    pulisci_schermo()
    stampa_separatore()
    print(" REPORT 2 - SPESE MENSILI VS BUDGET")
    stampa_separatore()

    cursore = conn.cursor()
    cursore.execute("""
        SELECT
            strftime('%Y-%m', s.data) AS mese,
            c.nome AS categoria,
            SUM(s.importo) AS speso,
            b.importo_budget AS budget
        FROM Spese s
        JOIN Categorie c ON s.categoria_id = c.ID
        LEFT JOIN Budget_mensile b
            ON strftime('%Y-%m', s.data) = b.Mese
            AND s.categoria_id = b.Categoria_id
        GROUP BY mese, c.nome
        ORDER BY mese, c.nome
    """)
    righe = cursore.fetchall()

    if not righe:
        print("\nNessuna spesa registrata.")
    else:
        mese_corrente = None
        for mese, categoria, speso, budget in righe:
            if mese != mese_corrente:
                print(f"\n  Mese: {mese}")
                stampa_separatore(45)
                print(f"  {'Categoria':<16} {'Speso':>7}  {'Budget':>7}  Stato")
                stampa_separatore(45)
                mese_corrente = mese

            if budget is None:
                stato = "Nessun budget"
            elif speso > budget:
                stato = "SUPERAMENTO BUDGET"
            else:
                stato = "HAI ANCORA BUDGET A DISPOSIZIONE"

            budget_str = f"{budget:.2f} €" if budget else "  N/D"
            print(f"  {categoria:<16} {speso:>6.2f} €  {budget_str:>7} {stato}")

    pausa()        
        
def report_elenco_spese(conn):
    pulisci_schermo()
    stampa_separatore()
    print(" REPORT 3 - ELENCO COMPLETO SPESE")
    stampa_separatore()

    cursore = conn.cursor()
    cursore.execute("""
        SELECT s.data, c.nome, s.importo, COALESCE(s.descrizione, '-')
        FROM Spese s
        JOIN Categorie c ON s.categoria_id = c.ID
        ORDER BY s.data ASC
    """)
    righe = cursore.fetchall()

    if not righe:
        print("\nNessuna spesa registrata.")
    else:
        print(f"\n{'Data':<14} {'Categoria':<18} {'Importo':>8}  Descrizione")
        stampa_separatore(60)
        for data, categoria, importo, descrizione in righe:
            print(f"{data:<14} {categoria:<18} {importo:>7.2f} €  {descrizione}")
        stampa_separatore(60)
        totale = sum(r[2] for r in righe)
        print(f"{'TOTALE':>34} {totale:>7.2f} €")

    pausa()
            
def menu_principale():
     conn = connetti_db()
     stampa_separatore()

     while True:
        print(" SISTEMA SPESE PERSONALI")
        stampa_separatore()
        print(" 1. Gestione Categorie")
        print(" 2. Inserisci Spesa")
        print(" 3. Definisci Budget Mensile")
        print(" 4. Visualizza Report")
        print(" 5. Esci")
        stampa_separatore()

        scelta = input(" Inserisci la tua scelta: ").strip()
        
        if scelta == "1":
            gestione_categorie(conn)
        elif scelta == "2":
            inserisci_spesa(conn)
        elif scelta == "3":
            definisci_budget(conn)
        elif scelta == "4":
            visualizza_report(conn)
        elif scelta == "5":
            print("\nArrivederci")
            conn.close()
            break
        else:
            print("\nScelta non valida. Riprova")
            pausa()
if __name__ == "__main__":
    menu_principale()
    

