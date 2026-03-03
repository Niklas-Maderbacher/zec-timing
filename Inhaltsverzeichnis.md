# Inhaltsverzeichnis ZEC-Timing

## Danksagung (beide zusammen ca 1 Seite)

## Kurzbeschreibung der Diplomarbeit (pro Person ca 1/2 Seite)

Ähnlicher Inhalt wie bei [Diplomarbeitsantrag](https://srhtblaweizac-my.sharepoint.com/:w:/g/personal/maderb190007_sr_htlweiz_at/IQA3pu9Pv9bTR6SpiOIgAI_XAYpv6PlvpApITMkNpQiFtDg?email=hmock%40lr.htlweiz.at&e=3rz6DP) (Seite 12 Punkt 15)

## Inhaltsverzeichnis (x Seiten)

## Individuelle Aufgabenstellung (pro Person ca 1 Seite)

Ausformulierte Aufgabenstellung aus [Diplomarbeitsantrag](https://srhtblaweizac-my.sharepoint.com/:w:/g/personal/maderb190007_sr_htlweiz_at/IQA3pu9Pv9bTR6SpiOIgAI_XAYpv6PlvpApITMkNpQiFtDg?email=hmock%40lr.htlweiz.at&e=3rz6DP) (Seite 10)

## Ziele (beide zusammen 1 Seite)

Ausformulierte Ziele aus [Diplomarbeitsantrag](https://srhtblaweizac-my.sharepoint.com/:w:/g/personal/maderb190007_sr_htlweiz_at/IQA3pu9Pv9bTR6SpiOIgAI_XAYpv6PlvpApITMkNpQiFtDg?email=hmock%40lr.htlweiz.at&e=3rz6DP) (Seite 10)

## Theoretische Grundlagen

### Containeriesierung (Niklas 2-3 Seiten)

Was Docker ist, wie es funktioniert und warum es Sinn macht es zu nutzen

### Microservices (Niklas 3-4 Seiten)

Wie Kubernetes funktioniert. Eventuell Unterschied zu Docker. Zusammenspiel von beidem

### MQtt (Niklas 1 bis max 2 Seiten)

Wie MQtt funktioniert (Publish/Subscribe)

### API und HTTP (David 1-2 Seiten)

Was eine API ist

## Systemarchitektur

### Überblick (großteiles David 2-3 Seiten)

alle Komponenten zusammen grafisch darstellen und kurz erklären

### Erklärung (großteils David 1-2 Seiten)

Wie alle Komponenten zusammenspielen

### Server (David 8-10 Seiten)

Alle Microservices nach der Reihe erklären + Datenbankschema (max 3 Tabellen pro Service) + Web App

### Desktop App (Niklas 2-3 Seiten)

Erklärung Kommunikation mit Server und MQtt (Zeitstempel)

## Implementation

### Server (David 8-9 Seiten wegen Screenshots)

Screenshot von Web App

API Gateway mit Beispielscode erklären. CRUD Operationen mit Beispielscode erklären. Authentifikation mit Keycloak. API mit Beispielscode erklären. Kommunikation zwischen den einzelnen Services mit Beispielcode erklären. Zugriffsberechtigungen je Rolle

### Desktop App (Niklas 2-3 Seiten)

Screenshot von Desktop App

Für einfachere Bereitstellung der Daten -> MQtt Zeitstempel über API zur Verfügung stellen. Zugriff auf Server mit Beispielscode erkären

### Github Workflows (Niklas 2-3 Seiten)

Github Workflows für automatisches builden der Container und hochladen in Github Container Registry + automatisches testen

### Kubernetes Cluster (Niklas 4-5 Seiten)

Deployment, Service, Ingres von k3s mit Beispielscode erklären.

## Testen und Deployment

### Testen (Niklas 3-4 Seiten)

Warum automatische Testcases nützlich sind und wie in Github Workflow eingebunden werden kann. Was abgetestet gehört + Negativ Testcases

#### Pytest (David 2-3 Seiten)

Testcase mit Beispielscode erklären. 

#### Playwright (Niklas 1-2 Seiten)

Testcase mit Beispielcode erklären

### Deployment

#### Deployment mit Docker (Niklas 1-2 Seiten)

Wie sich Server + Desktop App mittels Docker aufsetzen lassen. Worauf geachtet werden muss

#### Deployment mit Kubernetes (Niklas 2-4 Seiten)

Wie sich Server Services mittels Kubernetes aufsetzen lassen. Worauf geachtet werden muss

## Ergebnisse (beiden zusammen 1 Seite)

Was erreicht wurde

## Zukunfsausblick (insgesamt 3 bis max 4 Seiten)

### Datenbank Skalierungen (Niklas)

Datenbank wird aktuell nicht skaliert, sondern mittels Docker deployt

### Stand über Lichtschranke abrufen (Niklas)

Erweiterung auf Seite von Lichtschranke nötig

### SD Karten Schutz (David)

SD Karten Schutz derzeit nicht vorhanden. Implementation nötig, sofern Server auf RasPi läuft

## Resümee (beide zusammen 1 Seite)

Abschließende Worte über die Diplomarbeit

## Appendix

### Stundenverzeichnis (je 1 bis 1.5 Seiten. Insgesamt 3 Seiten)

### Technologieauswahl

#### GitHub (Niklas halbe Seite)

#### Docker (Niklas halbe Seite)

#### Kubernetes (Niklas halbe Seite)

#### MQtt (Niklas halbe Seite)

#### Redis (Niklas halbe Seite)

#### Postgres (David halbe Seite)

#### Keycloack (David halbe Seite)

#### SQLAlchemy (David halbe Seite)

#### FastAPI (David halbe Seite)

#### NextJs (David halbe Seite)

#### shadcn (David halbe Seite)

### Abbildungsverzeichnis (x Seiten)

### Quellenverzeichnis (x Seiten)