# RAIN BOT

Stylisches Python-CLI-Tool im Cyber-/Hacker-Look.

## Features

- ASCII-Art Banner mit Cyan->Magenta Gradient (`pyfiglet` + `colorama`)
- Animierte Matrix-Rain Intro-Animation
- Mehrstufige Loading-Bar mit Spinner, Prozent und Timer
- Interaktives Hauptmenue
- System-Info Anzeige (OS, Host, IP, Python-Version)

## Installation

```bash
pip install -r requirements.txt
```

## Start

```bash
python rainbot.py
```

## Voraussetzungen

- Python 3.9+
- Ein Terminal das ANSI-Farben unterstuetzt (Windows Terminal, iTerm2, GNOME Terminal, ...)

## Hinweise

- Auf Windows aktiviert `colorama` automatisch ANSI-Support.
- Die Rain-Animation passt sich an die Terminalgroesse an.
