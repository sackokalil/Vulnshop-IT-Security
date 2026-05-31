# VulnShop

VulnShop ist eine bewusst verwundbare E-Commerce-Webanwendung, die im Rahmen eines IT-Sicherheitsprojekts entwickelt wird. Das Projekt kombiniert einen einfachen Online-Shop mit einem Security-Lab, um verschiedene Web-Sicherheitslücken zu demonstrieren und deren Ausnutzung nachvollziehbar zu machen.

## Projektstatus

Das Projekt befindet sich derzeit in einer frühen Entwicklungsphase.

Aktuell sind hauptsächlich statische Platzhalterseiten implementiert, um die zukünftige Struktur der Anwendung vorzubereiten. Die Datenbankintegration sowie die meisten Geschäftslogiken werden in späteren Entwicklungsphasen ergänzt.

## Installation und Start

### 1. Repository klonen

```bash
git clone https://github.com/sackokalil/VulnShop.git
```

### 2. In das Projektverzeichnis wechseln

```bash
cd VulnShop
```

### 3. Virtuelle Umgebung erstellen
```bash
python -m venv .venv
```
### 4. Virtuelle Umgebung aktivieren
```bash
.venv\Scripts\activate
```
### 5. Abhängigkeiten installieren
```bash
pip install -r requirements.txt
```

### 6. Anwendung starten

```bash
python run.py
```

### 7. Anwendung im Browser öffnen

```text
http://127.0.0.1:5000
```

## Aktuell verfügbare Seiten

Folgende Routen können derzeit getestet werden:

### Shop

```text
http://127.0.0.1:5000/home
```

### Product details anzeigen : 
```text
Auf dem Product das fontawsom eye clicken
```

### Warenkorb anzeigen : 
```text
Auf dem Warenkorbszeichen oben rechts clicken
```

### Administration

```text
http://127.0.0.1:5000/admin/dashboard
```

## Aktueller Entwicklungsstand

Derzeit dienen die meisten Seiten lediglich als Platzhalter.

Folgende Funktionen sind noch nicht implementiert:

* Datenbankanbindung
* Dynamische Produktverwaltung
* Benutzerverwaltung
* Login-Funktion
* Registrierungsfunktion
* Warenkorb-Logik
* Bestellprozess
* Administrationsfunktionen

Die Produkt-, Kontakt-, Warenkorb- und Detailseiten verwenden aktuell statische Beispieldaten.

## Geplante Security-Lab-Komponente

Ein wichtiger Bestandteil des Projekts ist das integrierte Security-Lab.

Für jede Sicherheitslücke werden eigene Informationsseiten bereitgestellt, die unter anderem folgende Informationen enthalten:

* Beschreibung der Schwachstelle
* Betroffene Endpunkte
* Angriffsszenario
* Technische Hintergründe
* Beispielhafte Exploits
* Gegenmaßnahmen

Beispiele geplanter Themen:

* SQL Injection
* Cross-Site Scripting (XSS)
* Cross-Site Request Forgery (CSRF)
* Broken Access Control
* Authentication Vulnerabilities
* File Upload Vulnerabilities
* Path Traversal
* Command Injection

## Projektstruktur

### app.py

Die Datei `app.py` erstellt die Flask-Anwendung und registriert die verschiedenen Blueprints.

Beispielsweise:

* Home Blueprint
* Product Blueprint
* Contact Blueprint
* Admin Blueprint
* Security Lab Blueprint

### routes/

Die Dateien im Ordner `routes` enthalten ausschließlich das Routing.

Ihre Aufgabe besteht darin:

* HTTP-Anfragen entgegenzunehmen
* Anfragen an die Service-Schicht weiterzuleiten
* Die entsprechenden Templates zurückzugeben

Die eigentliche Geschäftslogik soll nicht direkt in den Routen implementiert werden.

### services/

Die Dateien im Ordner `services` bilden die Business-Logik-Schicht.

Sie übernehmen beispielsweise:

* Verarbeitung von Formulardaten
* Datenvalidierung
* Kommunikation mit der Datenbank
* Geschäftslogik
* DAO-Funktionalitäten (Data Access Objects)

### models/

Der Ordner `models` enthält die Datenmodelle der Anwendung.

Diese definieren unter anderem:

* Tabellenstrukturen
* Datenbankobjekte
* Beziehungen zwischen Entitäten

Beispiele:

* User
* Product
* Cart
* Order
* Review

### exploits/

Der Ordner `exploits` enthält Python-Skripte zur Demonstration von Angriffen.

Diese Skripte dienen ausschließlich zu Lern- und Demonstrationszwecken.

Die Exploits sollen zeigen, wie bestimmte Schwachstellen ausgenutzt werden können.

Beispiele:

* SQL-Injection-Skripte
* XSS-Demonstrationen
* CSRF-Demonstrationen
* Broken-Access-Control-Angriffe


