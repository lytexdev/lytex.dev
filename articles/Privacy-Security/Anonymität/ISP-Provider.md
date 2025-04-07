# ISP-Überwachung: Wie viel dein Internetanbieter über dich weiß

Ein ISP (Internet Service Provider) ist ein Internetanbieter, der dir den Zugang zum Internet bereitstellt. In Deutschland zählen dazu z. B.:
- Telekom
- Vodafone
- 1&1
- o2
- Lokale Anbieter oder Rechenzentren (bei Servern)

Sobald du online gehst – egal ob mit dem Handy, Laptop oder Smart-TV – läuft dein gesamter Datenverkehr zuerst durch die Infrastruktur deines ISPs. Er stellt dir deine IP-Adresse zur Verfügung, leitet deine Datenpakete weiter und regelt die Verbindung zwischen dir und dem Rest des Internets.

Damit ist der ISP technisch in der besten Position, deine Aktivitäten zu überwachen.

---

## Was kann der ISP grundsätzlich sehen?

Ohne zusätzliche Schutzmaßnahmen hat dein ISP technisch Zugriff auf:

- **Deine IP-Adresse** – die deinem Anschluss zugewiesen ist
- **Alle aufgerufenen IP-Adressen** – jede Domain, Webseite, App oder Dienst
- **DNS-Anfragen** – welche Domain du zu welchem Zeitpunkt aufrufst (z. B. `google.com`)
- **Zeitpunkte deiner Online-Aktivität** – wann du online warst, wie lange und mit welchem Datenvolumen
- **Unverschlüsselter Traffic** – wenn eine Webseite kein HTTPS nutzt (z. B. HTTP oder alte Protokolle), sind Inhalte vollständig im Klartext einsehbar

Das bedeutet: **selbst bei verschlüsselten Seiten kann dein ISP ein detailliertes Aktivitätsprofil erstellen – nur anhand von Metadaten**.

---

## Was bleibt für den ISP unsichtbar?

Wenn du HTTPS nutzt – was heute Standard ist –, kann dein ISP **nicht** sehen:

- Den **Inhalt der Webseiten** (z. B. was du auf einer Seite liest oder schreibst)
- **Passwörter, Formulare, Inhalte von Nachrichten**
- Den konkreten Seitenpfad (z. B. `/artikel/datenschutz` bleibt verborgen)
- Den Inhalt von **verschlüsselten Apps** (Signal, Matrix, im Browser etc.)

Aber: Er sieht trotzdem **wohin du gehst** (Domain), **wann** du dort bist und **wie viel** Daten du sendest/empfängst.

---

## Was ist SNI & warum ist es problematisch?

Beim Aufbau einer HTTPS-Verbindung wird in der Regel der sogenannte **Server Name Indication (SNI)** unverschlüsselt mitgeschickt. Dieser verrät dem ISP (und jeder Zwischenstelle), **welche Domain du besuchen willst**, bevor überhaupt eine TLS-Verbindung aufgebaut wird.

Beispiel:  
Du öffnest `https://signal.org` → SNI verrät dem ISP, dass du auf `signal.org` zugreifen willst – obwohl der Inhalt später verschlüsselt übertragen wird.

🔐 Abhilfe schafft hier **Encrypted SNI (ESNI)** bzw. der modernere Standard **ECH (Encrypted Client Hello)** – wird bisher aber nur von wenigen Browsern/Diensten unterstützt.

---

## Was passiert bei DNS-Anfragen?

DNS ist das „Telefonbuch“ des Internets. Wenn du eine Domain wie `google.com` aufrufst, wird dein Gerät eine DNS-Anfrage stellen, um die IP dahinter zu finden.

🔎 Diese Anfragen sind **standardmäßig unverschlüsselt** – der ISP sieht, **welche Domains du aufrufst**, auch wenn danach alles verschlüsselt ist.

✅ Lösung: **DNS over HTTPS (DoH)** oder **DNS over TLS (DoT)** aktivieren oder eigene DNS-Resolver (z. B. via `Pi-hole`, `NextDNS`, `Cloudflare`) nutzen.

---

## Was könnte dein ISP aus deinem Traffic ableiten?

Obwohl Inhalte verschlüsselt sind, sind viele **Muster und Verhaltensdaten** sichtbar:

- Welche Dienste du nutzt (z. B. Spotify, YouTube, Instagram – anhand IPs oder DNS)
- Tagesrhythmus: wann du online bist, wann du surfst, streamst oder zockst
- Traffic-Volumen: Uploads/Downloads, Datenverbrauch
- Wiederkehrende Aktivitäten: regelmäßige Besuche bei bestimmten Domains
- VPN-Nutzung (anhand bekannter VPN-IP-Ranges oder Protokolle wie WireGuard/OpenVPN)
- Wann man Tor nutzt (anhand der Tor-Node-IPs)

Das Ganze nennt man **Traffic Correlation** oder **Traffic Analysis** – und es ist ein mächtiges Werkzeug.

---

## Was kannst du dagegen tun?

**1. HTTPS konsequent nutzen**
- Moderne Browser tun das automatisch
- Nutze Browser, die Tracking & Mixed Content blockieren (z. B. Brave, LibreWolf)

**2. DNS absichern**
- Nutze DNS over HTTPS (DoH) oder TLS (DoT)
- Verwende vertrauenswürdige oder selbstgehostete DNS-Server

**3. VPN oder Tor nutzen**
- Ein VPN verschlüsselt den gesamten Traffic → Der ISP sieht nur, dass du mit einem VPN-Server verbunden bist
- Tor verschleiert deine Verbindung über mehrere Knoten → sehr effektiv gegen Traffic-Analyse, aber langsamer

**4. Keine Klartext-Protokolle verwenden**
- FTP, Telnet, HTTP vermeiden – sie übertragen Daten unverschlüsselt
- Alternative: SFTP, SSH, HTTPS

**5. ECH & SNI-Verschlüsselung aktivieren (falls möglich)**
- Firefox: `about:config` → `network.dns.echconfig.enabled = true`

---

## Fazit: Der ISP sieht mehr als man denkt – aber nicht alles

Auch wenn der Inhalt deiner Kommunikation verschlüsselt ist, bleibt dein Surfverhalten durch Metadaten weitgehend sichtbar. Dein ISP kann daraus ein überraschend genaues Profil deines Onlinelebens erstellen – ohne je eine Nachricht gelesen oder ein Bild gesehen zu haben.

✅ **Verschlüsselung ist der erste Schritt**  
✅ **Metadatenverschleierung (VPN, Tor, DNS-Schutz) der nächste**

Wenn du Privatsphäre wirklich ernst nimmst, solltest du deinen Traffic nicht nur verschlüsseln, sondern auch anonymisieren. Denn was dein ISP nicht sieht, kann er auch nicht speichern, auswerten oder weitergeben.
