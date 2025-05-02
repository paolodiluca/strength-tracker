Programm starten:



2 verschiedene Terminals

cd in den richtigen Ort (backend):
cd C:\Users\padil\strength-tracker

Umgebung starten:
.\venv\Scripts\activate
--> (venv) PS C:\Users\padil\strength-tracker> 

python app.py



2. Terminal: frontend starten:
cd C:\Users\padil\strength-tracker   
cd frontend
npm start



(APP öffnet sich im Browser)



Um App zu schließen: Im Backend Terminal CRTL+C drücken









==============================
STRENGTH TRACKER – INSTALLATION
==============================

📁 Projektübersicht:
--------------------
Ein vollständiges Webprojekt mit:
- Frontend (React) zur Eingabe & Anzeige von Trainingsdaten
- Backend (Flask + SQLite) zur Datenspeicherung
- Fortschrittsdiagramm mit 1-RM-Schätzung je Seite (Epley-Formel)

=======================
✅ 1. BENÖTIGTE INSTALLATIONEN
=======================

🔧 SYSTEMVORAUSSETZUNGEN:
-------------------------
- Python 3.x
- Node.js (npm wird mitinstalliert)
- (Optional: XAMPP – wird hier aber nicht genutzt)

🧰 VS CODE EMPFOHLENE ERWEITERUNGEN:
------------------------------------
- Python (Microsoft)
- ESLint
- Prettier
- SQLite Viewer (optional)
- React Developer Tools (für Chrome, nicht VS Code)

=======================
📦 2. BENÖTIGTE PAKETE
=======================

📁 BACKEND (Python / Flask):
----------------------------
Installieren mit:
    pip install flask flask_sqlalchemy flask_cors werkzeug

Oder per Datei:
    requirements.txt
    ---------------------
    flask
    flask_sqlalchemy
    flask_cors
    werkzeug

📁 FRONTEND (npm / React):
--------------------------
Im Verzeichnis `frontend/`:
    npm install react-datepicker date-fns

Automatisch vorhanden:
    - react
    - react-dom
    - react-scripts

=======================
🚀 3. START DES PROJEKTS
=======================

🔸 BACKEND:
-----------
    cd backend/
    python app.py

🔸 FRONTEND:
------------
    cd frontend/
    npm start

Dann öffnen im Browser:
    http://localhost:3000

=======================
ℹ️ 4. HINWEISE
=======================

- Die 1-RM-Berechnung (Kraftschätzung) funktioniert nur für 1–12 Wiederholungen.
- Wenn du mehr als 12 Reps eingibst, erscheint ein Hinweisbanner.
- Daten werden lokal in der Datei `strength.db` gespeichert.
