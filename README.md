# SkillPlate

SkillPlate ist eine umfassende Plattform zur Verwaltung von Kochkursen und Webinaren, entwickelt für den "Kunde e.V.".
Das System integriert moderne KI-Funktionen, um administrative Prozesse wie Kursplanung, Zertifizierung und
Rechnungsstellung zu automatisieren und zu optimieren.

## Funktionen

### Kursverwaltung

* Verwaltung von Präsenzkursen und Webinaren.
* Definition verschiedener Schwierigkeitsgrade.
* **KI-Unterstützung:** Generierung von Kursvorlagen, Rezeptideen und Strukturen.
* **Einkaufslisten (Webinare):** KI-generierte Einkaufslisten basierend auf Rezepten und lokalen Märkten (Kann-Ziel).

### Zertifizierung

* Überwachung des Teilnehmerfortschritts (Teilnehmerlisten/Logins).
* Automatische Erstellung und E-Mail-Versand von Zertifikaten nach Kursabschluss.

### Rechnungswesen

* **Eingangsrechnungen:** KI-gestützte Prüfung und Freigabe von Rechnungen unter einem Schwellenwert.
* **Ausgangsrechnungen:** Automatisierte Rechnungsstellung an Teilnehmer unter Berücksichtigung von Rabatten.

## Technologie-Stack

Das Projekt setzt auf eine moderne Container-Architektur:

* **Frontend:** Vue.js, Ionic, TypeScript, Vite
* **Backend:** Python, Flask, Gunicorn
* **Datenbank & REST:** Oracle Database Free, Oracle REST Data Services (ORDS)
* **Künstliche Intelligenz:** Ollama (Lokales LLM)
* **Containerisierung:** Docker, Docker Compose

## Installation und Start

### Voraussetzungen

* Docker
* Docker Compose

### Starten der Anwendung

Um das gesamte System zu starten, führen Sie folgenden Befehl im Hauptverzeichnis aus:

```bash
docker compose up --build -d
```

### Zugriff auf die Services

Nach dem Start sind die Dienste unter folgenden Adressen erreichbar:

* **Frontend:** [http://localhost:3000](http://localhost:3000)
* **Backend API:** [http://localhost:5000](http://localhost:5000)
* **ORDS (Datenbank-Schnittstelle):** [http://localhost:8080](http://localhost:8080)
* **Ollama API:** [http://localhost:11434](http://localhost:11434)

## Projektstruktur

* `backend/`: Quellcode für die Flask-API und ORDS-Konfigurationen.
* `frontend/`: Quellcode für das Vue.js/Ionic Frontend.
* `ollama/`: Konfigurationen für den KI-Service.
* `compose.yml`: Definition der Docker-Services und Netzwerke.
