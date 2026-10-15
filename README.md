# zec-timing Inbetriebnahme

GitHub Repository: https://github.com/Niklas-Maderbacher/zec-timing

## Requirements:
- Docker
- Kubernetes 

## Zeitnehmerapplikation

Die Zeitnehmerapplikation kann mittels `zeitnehmer_applikation.yml` gestartet werden und läuft anschließend auf `localhost:5173`. Hierbei zu beachten:
- `NEXT_PUBLIC_DESKTOP_APP_API_URL` auf den Hostname setzten, auf dem die `ZEC-API` läuft
- `NEXT_PUBLIC_MQTT_WORKER_API_URL` auf die IP-Adresse und Port setzten, auf dem der Mqtt-Worker läuft
- `NEXT_PUBLIC_API_KEY` auf den API-Key setzen, der bei der `ZEC-API` angegeben wurde.

Referenzwerte sind in `.env.example` zu finden.

Dieses Docker Compose File holt sich automatisch das benötigte Image aus der GitHub Container Registry

## Mqtt-Worker

Der MQTT-Worker kann mittels `mqtt_worker.yml` gestartet werden. Hierbei zu beachten:
- `MQTT_IP` **muss** auf den Container Namen des Mqtt-Brokers gesetzt werden
- `MQTT_PORT` **muss** auf `1883` gesetzt werden
- `MQTT_TOPIC` **muss** auf das Topic gesetzt werden, unter dem die Lichtschranke die Zeitstempel veröffentlicht
- `REDIS_HOST` **muss** auf den Container Namen der Redis Datenbank gesetzt werden
- `REDIS_PORT` **muss** auf `6379` gesetzt werden
- `TIMESTAMP_EXPIRE_TIME` **muss** auf die Zeit in Sekunden gesetzt werden, nach dem die Zeitstempel automatisch gelöscht werden.

Referenzwerte sind in `.env.example` zu finden.

## ZEC-API

Die `ZEC-API` kann im Verzeichnis `server-cluster` mit dem `start-stop.sh` Script gestartet werden. Hierbei zu beachten: Keycloak **muss** konfiguriert werden. Hierbei folgende Anleitung befolgen:

1. Nach dem Start mittels `kubectl port-forward deployment/keycloak-deployment 8080:8080` Keycloak von außer erreichbar machen.
2. Keycloak Admin Konsole unter `http://localhost:8080` aufrufen
    - Sollte die Admin Konsole nicht erreichbar sein und der Befehl in Schritt 1 fehlschlagen, etwa 5 Minuten warten bis Keycloak fertig gestartet hat und bei Schritt 1 wieder beginnen
    - Mittels `admin` als Nutzername und Passwort anmelden
3. Einen neuen Realm erstellen, in dem `realm_export.json` importiert wird.
4. Client Secrets erneuern
    1. Wechsle zu deinem neu erstellten **zec-realm**.
    2. Navigiere zu **Clients**.
    3. Öffne die Konfiguration des **login-client**.
    4. Wechsle zum Tab **Credentials** und generiere das Secret neu.
    5. Kopiere das neue **Secret**.
    6. Ändere den Wert in `deployment.yaml` beim `auth-service` (Zeile 115 und 117)
    7. Wiederhole die Schritte für den user-admin-client.
5. Änderungen mittels `kubectl apply -f deployment.yaml` übernehmen

