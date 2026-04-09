# Sistema di Gestione delle Spese Personali e del Budget

Applicazione console sviluppata in Python 3 con database SQLite
per la gestione delle spese personali, categorie e budget mensili.

Repository GitHub: https://github.com/Renatonototo5396/ProgettoInformatica

---

## Descrizione

Il sistema permette di:
- Aggiungere categorie di spesa personalizzate
- Registrare spese giornaliere con data, importo e categoria
- Definire budget mensili per categoria
- Visualizzare report riepilogativi sulle spese

---

## Requisiti

- Python 3.8 o superiore
- Nessuna libreria esterna (usa solo sqlite3, os, re)

---

## Come avviare il programma

1. Clona il repository:
git clone https://github.com/Renatonototo5396/ProgettoInformatica.git

2. Entra nella cartella:
cd ProgettoInformatica

3. Avvia il programma:
python3 src/main.py

---

## Struttura del progetto
ProgettoInformatica/
├── src/
│   └── main.py
├── sql/
│   └── database.sql
├── demo/
│   └── demo_video.mp4
└── README.md



---

## Struttura del database

Il database è composto da 3 tabelle:

- **Categorie** — contiene le categorie di spesa
- **Spese** — registra ogni singola spesa
- **Budget_mensile** — definisce il limite mensile per categoria

---

## Funzionalità principali

### Menu principale
1. Gestione Categorie
2. Inserisci Spesa
3. Definisci Budget Mensile
4. Visualizza Report
5. Esci

### Report disponibili
1. Totale spese per categoria
2. Spese mensili vs budget
3. Elenco completo spese ordinate per data