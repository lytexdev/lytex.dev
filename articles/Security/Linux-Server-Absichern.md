# Linux-Server Absichern

Ein Linux-Server ist eine leistungsstarke Basis fuer Webanwendungen, Datenbanken, Backups oder andere Dienste. Doch ohne die richtige Konfiguration kann er schnell zum Ziel von Angriffen werden. In diesem Post wird erklaert, wie man einen Linux-Server (in dem Fall Ubuntu) sicher einrichtet.

---

## Initiale Servereinrichtung

### Zugang per SSH einrichten
SSH ist der sicherste Weg, um auf deinen Server zuzugreifen.

1. **SSH-Keys generieren**:
   ```bash
   ssh-keygen -t ed25519 -C "email@example.com"
   ```
   Der private Schluessel bleibt auf deinem Computer, der oeffentliche Schluessel wird auf dem Server hinterlegt in der `authorized_keys` Datei gespeichert.

2. **SSH-Key auf den Server kopieren**:
   ```bash
   ssh-copy-id user@server-ip
   ```

3. **Passwortauthentifizierung deaktivieren**:
   oeffne die SSH-Konfigurationsdatei:
   ```bash
   sudo nano /etc/ssh/sshd_config
   ```
   aendere folgende Parameter:
   ```
   PasswordAuthentication no
   PermitRootLogin no
   ```

4. **SSH-Dienst neu starten**:
   ```bash
   sudo systemctl restart sshd
   ```

### System-Updates installieren
Halte dein System immer aktuell, um Sicherheitsluecken zu schließen:
```bash
sudo apt update && sudo apt upgrade -y
```

#### Automatische Sicherheitsupdates aktivieren
1. **Paket `unattended-upgrades` installieren**:
   ```bash
   sudo apt install unattended-upgrades
   ```

2. **Automatische Updates aktivieren**:
   Konfiguriere das System, um automatische Sicherheitsupdates zu ermoeglichen:
   ```bash
   sudo dpkg-reconfigure --priority=low unattended-upgrades
   ```
   Waehle im Dialog **Yes**, um die Funktion zu aktivieren.

3. **Anpassung der Update-Einstellungen (optional)**:
   oeffne die Datei `/etc/apt/apt.conf.d/50unattended-upgrades`:
   ```bash
   sudo nano /etc/apt/apt.conf.d/50unattended-upgrades
   ```
   Stelle sicher, dass folgende Zeilen vorhanden sind (ohne Kommentarzeichen `//`):
   ```
   Unattended-Upgrade::Allowed-Origins {
       "${distro_id}:${distro_codename}-security";
   };
   ```

4. **Automatische Ausfuehrung festlegen**:
   Passe die Datei `/etc/apt/apt.conf.d/10periodic` an, um das Update-Intervall zu steuern:
   ```bash
   sudo nano /etc/apt/apt.conf.d/10periodic
   ```
   Fuege die folgenden Zeilen hinzu oder aendere die Werte nach Bedarf:
   ```
   APT::Periodic::Update-Package-Lists "1";
   APT::Periodic::Download-Upgradeable-Packages "1";
   APT::Periodic::AutocleanInterval "7";
   APT::Periodic::Unattended-Upgrade "1";
   ```

5. **Updates testen**:
   Simuliere die automatische Aktualisierung mit:
   ```bash
   sudo unattended-upgrades --dry-run
   ```

6. **Protokolle ueberpruefen**:
   Automatische Updates werden hier protokolliert:
   ```bash
   cat /var/log/unattended-upgrades/unattended-upgrades.log
   ```

Mit dieser Einrichtung bleibt dein System immer auf dem neuesten Stand, was das Risiko von Sicherheitsluecken erheblich reduziert.

---

## Benutzer- und Rechteverwaltung

### Root-Login deaktivieren
Root hat unbegrenzte Rechte und ist ein beliebtes Angriffsziel. Stelle sicher, dass sich niemand direkt als Root anmelden kann..:

Bearbeite die Datei `/etc/ssh/sshd_config`:
```
PermitRootLogin no
```
Starte den SSH-Dienst neu:
```bash
sudo systemctl restart sshd
```

### Benutzer mit eingeschraenkten Rechten anlegen
Lege einen Benutzer an:
```bash
sudo adduser user
sudo usermod -aG sudo user
```

---

## Firewall und Netzwerkabsicherung

### Firewall mit UFW konfigurieren
1. **UFW installieren und konfigurieren**:
   ```bash
   sudo apt install ufw
   sudo ufw allow 22/tcp # Um SSH / Port 22 ueber TCP zu erlauben
   sudo ufw enable
   ```

2. **Dienste explizit erlauben**:
   ```bash
   sudo ufw allow 443  # HTTPS
   sudo ufw allow 80/tcp   # HTTP | Dienste mit explizitem Port
   ```

3. **Firewall-Status ueberpruefen**:
   ```bash
   sudo ufw status verbose
   ```

## Intrusion Detection und Monitoring

### Fail2Ban installieren und konfigurieren
Fail2Ban schuetzt vor Brute-Force-Angriffen, da nach einer bestimmten Anzahl an eingegebenen Passwoertern, der Nutzer fuer eine Zeit gesperrt wird.

1. **Installation**:
   ```bash
   sudo apt install fail2ban
   ```

2. **Konfigurationsdatei erstellen**:
   ```bash
   sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
   sudo nano /etc/fail2ban/jail.local
   ```
   Stelle sicher, dass SSH geschuetzt ist:
   ```
   [sshd]
   enabled = true
   port = 22
   ```

3. **Fail2Ban starten**:
   ```bash
   sudo systemctl enable --now fail2ban
   ```

---

## Automatische Backups einrichten
Sichere regelmaeßig deine Daten.

1. **rsync-Skript erstellen**:
   ```bash
   #!/bin/bash
   rsync -avz /wichtig/verzeichnis backup-user@backup-server:/backup-pfad
   ```
2. **Automatisieren mit Cron**:
   ```bash
   crontab -e
   ```
   Beispiel: Taegliches Backup um 2 Uhr nachts:
   ```
   0 2 * * * /pfad/zum/backup-script.sh
   ```
3. **Unser remote backup script**: [Gitea Repository](https://git.lytex.dev/lytex/remote-backup)

---

## Zusaetzliche Tipps und Tools
- **SELinux** oder **AppArmor** aktivieren, um Prozesse zu isolieren.
- Verwende **knockd**, um versteckte Ports zu schuetzen, in dem man an andere Ports vorher anklopfen muss
- Installiere **Lynis**, um Sicherheitschecks auf deinem Server auszufuehren:
  ```bash
  sudo apt install lynis
  sudo lynis audit system
  ```

---

Mit diesen Schritten richtest du deinen Linux-Server sicher ein und bist besser vor Angriffen gut geschuetzt. Denk daran, regelmaeßig Updates durchzufuehren und dein System zu ueberwachen!
