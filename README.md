# 📦 Guida all’installazione e avvio del progetto

Questo progetto richiede Python e un ambiente virtuale (venv) incluso nella cartella.

La guida seguente spiega come avviarlo su Windows tramite Prompt dei comandi.

---

## 1. INSTALLARE PYTHON

Se Python non è installato:

- Vai su https://www.python.org/downloads/
- Scarica l’ultima versione per Windows
- Durante l’installazione:
  - spunta **Add Python to PATH**
  - clicca su **Install Now**

---

## 2. APRIRE LA CARTELLA DEL PROGETTO

- Estrai la cartella del progetto se è in `.zip`
- Apri la cartella
- Clicca sulla barra del percorso in alto
- Scrivi `cmd`
- Premi INVIO

Si aprirà il Prompt dei comandi nella cartella giusta.

---

## 3. ATTIVARE L’AMBIENTE VIRTUALE

Nel Prompt dei comandi scrivi:

```bash
venv\Scripts\activate
```

Se tutto funziona correttamente vedrai:

```
(venv)
```

all’inizio della riga.

---

## 4. INSTALLARE LE DIPENDENZE

Se è presente il file `requirements.txt`, esegui:

```bash
pip install -r requirements.txt
```

---

## 5. AVVIARE IL PROGETTO

Esegui il file principale:

```bash
python main.py
```

oppure:

```bash
python app.py
```

---

## 6. PROBLEMI COMUNI

### ❌ "python non è riconosciuto"
- Python non è nel PATH
- Reinstalla Python e spunta **Add Python to PATH**

### ❌ "venv non trovato"
- Non sei nella cartella corretta del progetto

### 🔧 Creazione manuale ambiente virtuale

```bash
py -m venv venv
```

---

## NOTE FINALI

- Non cancellare la cartella `venv`
- Non spostare i file del progetto
- Aprire sempre il terminale nella cartella corretta