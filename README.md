# RAIN BOT

Stylisches Python-CLI-Tool im Cyber-/Hacker-Look mit echten Tools.

## Intro
1. Matrix-Rain Animation
2. ASCII-Banner "RAIN BOT" mit Cyan->Magenta Gradient
3. Animierte Loading-Bars (Boot-Sequenz)
4. Roter Devil-ASCII-Art (doxbin style)
5. Tools-Menue

## Tools

| # | Tool | Beschreibung |
|---|------|--------------|
| 1 | IP Lookup          | Geo / ISP / ASN via ip-api.com (kein API-Key) |
| 2 | Webhook Sender     | Sendet Nachrichten an Discord-Webhooks |
| 3 | Port Scanner       | Multi-threaded TCP Port-Scan (common / range / custom) |
| 4 | Hash Generator     | MD5 / SHA1 / SHA256 / SHA512 fuer Strings oder Dateien |
| 5 | Password Generator | Sichere Zufallspasswoerter (`secrets`-Modul) |
| 9 | Show Devil         | Devil-Bild nochmal anzeigen |
| 0 | Exit               | Beenden |

## Installation

```bash
pip install -r requirements.txt
```

`colorama` und `pyfiglet` sind **optional** - ohne sie laeuft das Tool auch (mit Fallback-Banner und ohne Farben).

## Start

```bash
python rainbot.py
```

## Voraussetzungen

- Python 3.9+
- Terminal mit ANSI-Farb-Support (Windows Terminal, iTerm2, etc.)

## Disclaimer

Dieses Tool ist fuer **Bildungszwecke** und legitimes Testing **eigener** Systeme. Port-Scans und aehnliches nur auf Systemen anwenden, fuer die eine Berechtigung besteht.
