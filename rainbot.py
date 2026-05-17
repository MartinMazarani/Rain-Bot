#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAIN BOT
--------
Stylisches CLI-Tool im Cyber-/Hacker-Look mit:
  * Matrix-Style "Rain"-Intro
  * Animierter Loading-Bar
  * Roter Devil-ASCII-Art (doxbin style)
  * 5 echte Tools (IP Lookup, Webhook, Port Scan, Hash, Password)
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import random
import secrets
import shutil
import socket
import string
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import List

# ---------------------------------------------------------------------------
# Optional deps
# ---------------------------------------------------------------------------

try:
    from colorama import Fore, Style, init as colorama_init
    colorama_init(autoreset=True)
except ImportError:
    class _Dummy:
        def __getattr__(self, _): return ""
    Fore = Style = _Dummy()  # type: ignore

try:
    import pyfiglet  # type: ignore
    HAS_PYFIGLET = True
except ImportError:
    HAS_PYFIGLET = False


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

AUTHOR = "proxytq"
VERSION = "1.1.0"
TOOL_NAME = "RAIN BOT"

GRADIENT = [
    Fore.CYAN, Fore.LIGHTCYAN_EX, Fore.LIGHTBLUE_EX,
    Fore.BLUE, Fore.LIGHTMAGENTA_EX, Fore.MAGENTA,
]

RED_GRADIENT = [
    Fore.LIGHTRED_EX, Fore.RED, Fore.RED,
    Fore.LIGHTRED_EX, Fore.RED, Fore.LIGHTRED_EX,
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def term_size() -> tuple[int, int]:
    s = shutil.get_terminal_size(fallback=(100, 30))
    return s.columns, s.lines


def center_block(text: str) -> str:
    cols = term_size()[0]
    return "\n".join(line.center(cols) for line in text.splitlines())


def gradient_text(text: str, colors: List[str] = GRADIENT) -> str:
    out = []
    for i, line in enumerate(text.splitlines()):
        out.append(f"{colors[i % len(colors)]}{line}{Style.RESET_ALL}")
    return "\n".join(out)


def banner_line(label: str) -> None:
    cols = term_size()[0]
    bar = "-" * min(cols - 4, 60)
    print(f"  {Fore.LIGHTBLACK_EX}{bar}{Style.RESET_ALL}")
    print(f"  {Fore.LIGHTMAGENTA_EX}>> {Fore.WHITE}{label}{Style.RESET_ALL}")
    print(f"  {Fore.LIGHTBLACK_EX}{bar}{Style.RESET_ALL}")


def pause() -> None:
    input(f"\n  {Fore.LIGHTBLACK_EX}[ENTER] zurueck zum Menue...{Style.RESET_ALL}")


# ---------------------------------------------------------------------------
# Matrix Rain
# ---------------------------------------------------------------------------

def matrix_rain(duration: float = 1.5) -> None:
    cols, _ = term_size()
    charset = "01abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ#@$%&*+="
    end = time.time() + duration
    clear()
    while time.time() < end:
        line = "".join(
            random.choice(charset) if random.random() > 0.25 else " "
            for _ in range(cols)
        )
        shade = random.choice([Fore.GREEN, Fore.LIGHTGREEN_EX])
        print(f"{shade}{line}{Style.RESET_ALL}")
        time.sleep(0.04)
    clear()


# ---------------------------------------------------------------------------
# RAIN BOT Banner
# ---------------------------------------------------------------------------

BUILTIN_BANNER = r"""
 ______       _      _____ _   _    ______  _____  _____
 | ___ \     (_)    |_   _| \ | |   | ___ \|  _  ||_   _|
 | |_/ /__ _  _ _ __  | | |  \| |   | |_/ /| | | |  | |
 |    // _` || | '_ \ | | | . ` |   | ___ \| | | |  | |
 | |\ \ (_| || | | | || |_| |\  |   | |_/ /\ \_/ /  | |
 \_| \_\__,_||_|_| |_\___/\_| \_/   \____/  \___/   \_/
"""


def render_main_banner() -> str:
    if HAS_PYFIGLET:
        return gradient_text(pyfiglet.figlet_format(TOOL_NAME, font="ansi_shadow"))
    return gradient_text(BUILTIN_BANNER)


def print_main_banner() -> None:
    cols = term_size()[0]
    print()
    for line in render_main_banner().splitlines():
        pad = max((cols - len(line)) // 2, 0)
        print(" " * pad + line)
    bar = f"{Fore.LIGHTBLACK_EX}{'-' * min(cols - 4, 70)}{Style.RESET_ALL}"
    info = (
        f"{Fore.LIGHTCYAN_EX}>> {Fore.WHITE}Author : {Fore.LIGHTMAGENTA_EX}{AUTHOR}"
        f"   {Fore.WHITE}Version: {Fore.LIGHTMAGENTA_EX}v{VERSION}"
        f"   {Fore.WHITE}Build  : {Fore.LIGHTMAGENTA_EX}{datetime.now():%Y-%m-%d}"
    )
    print()
    print(center_block(bar))
    print(center_block(info))
    print(center_block(bar))
    print()


# ---------------------------------------------------------------------------
# Devil Banner (doxbin style)
# ---------------------------------------------------------------------------

DEVIL_ART = r'''
                       _,...,_
                    .-'       `-.
                  ,'    _   _    `.
                 /    /(o) (o)\    \
                ;    /   ^^^   \    ;
                |   |  (  Y  )  |   |
                ;    \   \_/   /    ;
                 \    `.,___,.'    /
                  `.   _____    ,'
                    `-'     `--'
              \\\\\           /////
              \\\\\\         //////
              =\\\\\\       //////=
                \V/  \\___//  \V/
                 ||   |||||   ||
                 ||   |||||   ||
                 W    \|||/    W
                       VVV
                      _|_|_
                     /__|__\
                    /_/   \_\

         .-.   .-.   .-.   .-.   .-.   .-.   .-.   .-.
        ( 6 ) ( 6 ) ( 6 ) ( 6 ) ( 6 ) ( 6 ) ( 6 ) ( 6 )
         `-'   `-'   `-'   `-'   `-'   `-'   `-'   `-'

              [   W E L C O M E   T O   H E L L   ]
                       proxytq // rain bot
'''


def print_devil() -> None:
    """Druckt das Devil-Bild in rot mit kleinem Fade-In."""
    clear()
    cols = term_size()[0]
    lines = DEVIL_ART.splitlines()
    for i, line in enumerate(lines):
        color = RED_GRADIENT[i % len(RED_GRADIENT)]
        pad = max((cols - len(line)) // 2, 0)
        sys.stdout.write(" " * pad + f"{Style.BRIGHT}{color}{line}{Style.RESET_ALL}\n")
        sys.stdout.flush()
        time.sleep(0.03)
    print()
    sub = f"{Fore.RED}>> {Fore.LIGHTRED_EX}{AUTHOR}{Fore.RED} :: {Fore.WHITE}all systems compromised{Style.RESET_ALL}"
    print(center_block(sub))
    print()
    time.sleep(1.2)


# ---------------------------------------------------------------------------
# Loading Bar
# ---------------------------------------------------------------------------

SPINNER = ["|", "/", "-", "\\"]


def loading_bar(label: str, duration: float = 1.0, width: int = 38) -> None:
    steps = 100
    delay = duration / steps
    start = time.time()
    for i in range(steps + 1):
        filled = int(width * i / steps)
        empty = width - filled
        bar_filled = ""
        for j in range(filled):
            color = GRADIENT[(j * len(GRADIENT) // max(width, 1)) % len(GRADIENT)]
            bar_filled += f"{color}#{Style.RESET_ALL}"
        bar_empty = f"{Fore.LIGHTBLACK_EX}{'-' * empty}{Style.RESET_ALL}"
        spin = SPINNER[i % len(SPINNER)]
        elapsed = time.time() - start
        line = (
            f"  {Fore.LIGHTMAGENTA_EX}[{spin}]{Style.RESET_ALL} "
            f"{Fore.WHITE}{label:<22}{Style.RESET_ALL} "
            f"{Fore.LIGHTBLACK_EX}[{Style.RESET_ALL}"
            f"{bar_filled}{bar_empty}"
            f"{Fore.LIGHTBLACK_EX}]{Style.RESET_ALL} "
            f"{Fore.LIGHTCYAN_EX}{i:3d}%{Style.RESET_ALL} "
            f"{Fore.LIGHTBLACK_EX}({elapsed:4.1f}s){Style.RESET_ALL}"
        )
        sys.stdout.write("\r" + line)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def boot_sequence() -> None:
    tasks = [
        ("Loading core ........", 1.0),
        ("Connecting sockets ..", 0.9),
        ("Decrypting modules ..", 1.2),
        ("Spawning workers ....", 0.8),
        ("Summoning daemons ...", 1.0),
        ("Finalizing ..........", 0.6),
    ]
    print()
    for label, dur in tasks:
        loading_bar(label, dur)
    print(f"\n  {Fore.LIGHTGREEN_EX}[OK]{Style.RESET_ALL} "
          f"{Fore.WHITE}All systems online.{Style.RESET_ALL}\n")
    time.sleep(0.5)


# ---------------------------------------------------------------------------
# Tool 1: IP Lookup (ip-api.com - kein API key noetig)
# ---------------------------------------------------------------------------

def tool_ip_lookup() -> None:
    banner_line("IP LOOKUP")
    target = input(f"  {Fore.LIGHTCYAN_EX}IP / Domain "
                   f"{Fore.LIGHTBLACK_EX}(leer = eigene IP){Fore.WHITE}: {Style.RESET_ALL}").strip()
    url = f"http://ip-api.com/json/{urllib.parse.quote(target)}" if target else "http://ip-api.com/json/"
    try:
        with urllib.request.urlopen(url, timeout=8) as r:
            data = json.loads(r.read().decode())
    except (urllib.error.URLError, socket.timeout) as e:
        print(f"  {Fore.LIGHTRED_EX}[!] Fehler: {e}{Style.RESET_ALL}")
        return pause()

    if data.get("status") != "success":
        print(f"  {Fore.LIGHTRED_EX}[!] {data.get('message', 'unknown error')}{Style.RESET_ALL}")
        return pause()

    fields = [
        ("IP",       "query"),
        ("Country",  "country"),
        ("Region",   "regionName"),
        ("City",     "city"),
        ("ZIP",      "zip"),
        ("Lat/Lon",  None),
        ("Timezone", "timezone"),
        ("ISP",      "isp"),
        ("Org",      "org"),
        ("AS",       "as"),
    ]
    print()
    for label, key in fields:
        if label == "Lat/Lon":
            val = f"{data.get('lat')}, {data.get('lon')}"
        else:
            val = data.get(key, "-")
        print(f"  {Fore.LIGHTCYAN_EX}{label:<9}{Style.RESET_ALL} "
              f"{Fore.LIGHTBLACK_EX}:{Style.RESET_ALL} "
              f"{Fore.WHITE}{val}{Style.RESET_ALL}")
    pause()


# ---------------------------------------------------------------------------
# Tool 2: Webhook Sender (Discord)
# ---------------------------------------------------------------------------

def tool_webhook() -> None:
    banner_line("WEBHOOK SENDER")
    print(f"  {Fore.LIGHTBLACK_EX}Sendet eine Nachricht an einen Discord-Webhook.{Style.RESET_ALL}\n")
    url = input(f"  {Fore.LIGHTCYAN_EX}Webhook URL{Fore.WHITE}: {Style.RESET_ALL}").strip()
    if not url.startswith(("https://discord.com/api/webhooks/", "https://discordapp.com/api/webhooks/")):
        print(f"  {Fore.LIGHTRED_EX}[!] Ungueltige Discord-Webhook-URL.{Style.RESET_ALL}")
        return pause()

    username = input(f"  {Fore.LIGHTCYAN_EX}Username     {Fore.LIGHTBLACK_EX}(optional){Fore.WHITE}: {Style.RESET_ALL}").strip()
    content  = input(f"  {Fore.LIGHTCYAN_EX}Message      {Fore.WHITE}: {Style.RESET_ALL}").strip()
    try:
        count = int(input(f"  {Fore.LIGHTCYAN_EX}Wie oft senden {Fore.LIGHTBLACK_EX}(default 1){Fore.WHITE}: {Style.RESET_ALL}") or "1")
    except ValueError:
        count = 1
    count = max(1, min(count, 50))  # safety cap

    if not content:
        print(f"  {Fore.LIGHTRED_EX}[!] Leere Nachricht abgebrochen.{Style.RESET_ALL}")
        return pause()

    payload = {"content": content}
    if username:
        payload["username"] = username
    body = json.dumps(payload).encode()

    print()
    ok = fail = 0
    for i in range(1, count + 1):
        req = urllib.request.Request(
            url, data=body,
            headers={"Content-Type": "application/json", "User-Agent": "RainBot/1.1"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=8) as r:
                if 200 <= r.status < 300:
                    print(f"  {Fore.LIGHTGREEN_EX}[OK]{Style.RESET_ALL} "
                          f"#{i} sent ({r.status})")
                    ok += 1
                else:
                    print(f"  {Fore.LIGHTRED_EX}[!]{Style.RESET_ALL} "
                          f"#{i} status {r.status}")
                    fail += 1
        except urllib.error.HTTPError as e:
            print(f"  {Fore.LIGHTRED_EX}[!]{Style.RESET_ALL} #{i} HTTP {e.code}: {e.reason}")
            fail += 1
        except Exception as e:
            print(f"  {Fore.LIGHTRED_EX}[!]{Style.RESET_ALL} #{i} {e}")
            fail += 1
        time.sleep(0.6)  # rate-limit friendly

    print(f"\n  {Fore.LIGHTMAGENTA_EX}>> {Fore.WHITE}Done. "
          f"{Fore.LIGHTGREEN_EX}{ok} ok{Fore.WHITE} / "
          f"{Fore.LIGHTRED_EX}{fail} fail{Style.RESET_ALL}")
    pause()


# ---------------------------------------------------------------------------
# Tool 3: Port Scanner
# ---------------------------------------------------------------------------

COMMON_PORTS = [
    21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445,
    993, 995, 1723, 3306, 3389, 5432, 5900, 6379, 8000, 8080, 8443, 27017,
]


def _scan_port(host: str, port: int, timeout: float) -> int | None:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            if s.connect_ex((host, port)) == 0:
                return port
    except Exception:
        pass
    return None


def tool_port_scan() -> None:
    banner_line("PORT SCANNER")
    host = input(f"  {Fore.LIGHTCYAN_EX}Target host/IP{Fore.WHITE}: {Style.RESET_ALL}").strip()
    if not host:
        return
    mode = input(f"  {Fore.LIGHTCYAN_EX}Mode {Fore.LIGHTBLACK_EX}"
                 f"[1] common  [2] range  [3] custom{Fore.WHITE}: {Style.RESET_ALL}").strip()

    if mode == "2":
        try:
            lo = int(input(f"  {Fore.LIGHTCYAN_EX}From{Fore.WHITE}: {Style.RESET_ALL}"))
            hi = int(input(f"  {Fore.LIGHTCYAN_EX}To  {Fore.WHITE}: {Style.RESET_ALL}"))
        except ValueError:
            print(f"  {Fore.LIGHTRED_EX}[!] ungueltige Eingabe{Style.RESET_ALL}")
            return pause()
        ports = list(range(max(1, lo), min(65535, hi) + 1))
    elif mode == "3":
        raw = input(f"  {Fore.LIGHTCYAN_EX}Ports (kommasepariert){Fore.WHITE}: {Style.RESET_ALL}")
        try:
            ports = [int(p) for p in raw.replace(" ", "").split(",") if p]
        except ValueError:
            print(f"  {Fore.LIGHTRED_EX}[!] ungueltige Ports{Style.RESET_ALL}")
            return pause()
    else:
        ports = COMMON_PORTS

    try:
        ip = socket.gethostbyname(host)
    except socket.gaierror:
        print(f"  {Fore.LIGHTRED_EX}[!] Host nicht aufloesbar.{Style.RESET_ALL}")
        return pause()

    print(f"\n  {Fore.LIGHTMAGENTA_EX}>> {Fore.WHITE}Scanning "
          f"{Fore.LIGHTCYAN_EX}{host} ({ip}){Fore.WHITE} - "
          f"{Fore.LIGHTCYAN_EX}{len(ports)} ports{Style.RESET_ALL}\n")

    open_ports = []
    start = time.time()
    with ThreadPoolExecutor(max_workers=200) as ex:
        futures = {ex.submit(_scan_port, ip, p, 0.6): p for p in ports}
        for fut in as_completed(futures):
            port = fut.result()
            if port:
                try:
                    svc = socket.getservbyport(port)
                except OSError:
                    svc = "?"
                open_ports.append((port, svc))
                print(f"  {Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} "
                      f"{Fore.WHITE}{port:>5}/tcp{Style.RESET_ALL}  "
                      f"{Fore.LIGHTBLACK_EX}{svc}{Style.RESET_ALL}")

    dur = time.time() - start
    print(f"\n  {Fore.LIGHTMAGENTA_EX}>> {Fore.WHITE}Done. "
          f"{Fore.LIGHTGREEN_EX}{len(open_ports)} open{Fore.WHITE} / "
          f"{len(ports)} scanned in "
          f"{Fore.LIGHTCYAN_EX}{dur:.2f}s{Style.RESET_ALL}")
    pause()


# ---------------------------------------------------------------------------
# Tool 4: Hash Generator
# ---------------------------------------------------------------------------

def tool_hash() -> None:
    banner_line("HASH GENERATOR")
    src = input(f"  {Fore.LIGHTCYAN_EX}Source {Fore.LIGHTBLACK_EX}[1] string  [2] file{Fore.WHITE}: {Style.RESET_ALL}").strip()
    if src == "2":
        path = input(f"  {Fore.LIGHTCYAN_EX}File path{Fore.WHITE}: {Style.RESET_ALL}").strip()
        if not os.path.isfile(path):
            print(f"  {Fore.LIGHTRED_EX}[!] Datei nicht gefunden.{Style.RESET_ALL}")
            return pause()
        hashes = {a: hashlib.new(a) for a in ("md5", "sha1", "sha256", "sha512")}
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                for h in hashes.values():
                    h.update(chunk)
        results = {a: h.hexdigest() for a, h in hashes.items()}
        label = path
    else:
        text = input(f"  {Fore.LIGHTCYAN_EX}Text{Fore.WHITE}: {Style.RESET_ALL}")
        data = text.encode()
        results = {
            "md5":    hashlib.md5(data).hexdigest(),
            "sha1":   hashlib.sha1(data).hexdigest(),
            "sha256": hashlib.sha256(data).hexdigest(),
            "sha512": hashlib.sha512(data).hexdigest(),
        }
        label = f'"{text}"' if len(text) <= 40 else f'"{text[:37]}..."'

    print(f"\n  {Fore.LIGHTBLACK_EX}Source: {Fore.WHITE}{label}{Style.RESET_ALL}\n")
    for algo, digest in results.items():
        print(f"  {Fore.LIGHTCYAN_EX}{algo.upper():<7}{Style.RESET_ALL} "
              f"{Fore.LIGHTBLACK_EX}:{Style.RESET_ALL} "
              f"{Fore.WHITE}{digest}{Style.RESET_ALL}")
    pause()


# ---------------------------------------------------------------------------
# Tool 5: Password Generator
# ---------------------------------------------------------------------------

def tool_password() -> None:
    banner_line("PASSWORD GENERATOR")
    try:
        length = int(input(f"  {Fore.LIGHTCYAN_EX}Length {Fore.LIGHTBLACK_EX}(default 20){Fore.WHITE}: {Style.RESET_ALL}") or "20")
        count  = int(input(f"  {Fore.LIGHTCYAN_EX}How many {Fore.LIGHTBLACK_EX}(default 5){Fore.WHITE}: {Style.RESET_ALL}") or "5")
    except ValueError:
        print(f"  {Fore.LIGHTRED_EX}[!] ungueltige Zahl{Style.RESET_ALL}")
        return pause()

    length = max(4, min(length, 128))
    count  = max(1, min(count, 50))

    use_sym = input(f"  {Fore.LIGHTCYAN_EX}Symbols? {Fore.LIGHTBLACK_EX}[Y/n]{Fore.WHITE}: {Style.RESET_ALL}").strip().lower() != "n"
    alphabet = string.ascii_letters + string.digits + (string.punctuation if use_sym else "")

    print()
    for i in range(1, count + 1):
        pw = "".join(secrets.choice(alphabet) for _ in range(length))
        # Faerbung pro Zeichen-Klasse
        colored = ""
        for ch in pw:
            if ch.isdigit():
                colored += f"{Fore.LIGHTCYAN_EX}{ch}"
            elif ch.isalpha():
                colored += f"{Fore.WHITE}{ch}"
            else:
                colored += f"{Fore.LIGHTMAGENTA_EX}{ch}"
        print(f"  {Fore.LIGHTBLACK_EX}{i:>2}.{Style.RESET_ALL} {colored}{Style.RESET_ALL}")
    pause()


# ---------------------------------------------------------------------------
# Menu
# ---------------------------------------------------------------------------

MENU_ITEMS = [
    ("1", "IP Lookup",          "Geo / ISP / ASN via ip-api"),
    ("2", "Webhook Sender",     "Sende Nachrichten an Discord-Webhooks"),
    ("3", "Port Scanner",       "Multi-threaded TCP Port Scan"),
    ("4", "Hash Generator",     "MD5 / SHA1 / SHA256 / SHA512"),
    ("5", "Password Generator", "Sichere Zufallspasswoerter"),
    ("9", "Show Devil",         "Devil-Bild nochmal anzeigen"),
    ("0", "Exit",               "Tool beenden"),
]


def print_menu() -> None:
    print(f"  {Fore.LIGHTMAGENTA_EX}>> {Fore.WHITE}TOOLS{Style.RESET_ALL}")
    print(f"  {Fore.LIGHTBLACK_EX}{'-' * 60}{Style.RESET_ALL}")
    for key, name, desc in MENU_ITEMS:
        print(
            f"  {Fore.LIGHTCYAN_EX}[{key}]{Style.RESET_ALL} "
            f"{Fore.WHITE}{name:<20}{Style.RESET_ALL}"
            f"{Fore.LIGHTBLACK_EX}{desc}{Style.RESET_ALL}"
        )
    print()


def prompt() -> str:
    return input(
        f"  {Fore.LIGHTRED_EX}root@rainbot{Fore.WHITE}:"
        f"{Fore.LIGHTCYAN_EX}~{Fore.WHITE}$ {Style.RESET_ALL}"
    ).strip()


HANDLERS = {
    "1": tool_ip_lookup,
    "2": tool_webhook,
    "3": tool_port_scan,
    "4": tool_hash,
    "5": tool_password,
}


def main_loop() -> None:
    while True:
        clear()
        print_main_banner()
        print_menu()
        choice = prompt()
        print()
        if choice in HANDLERS:
            try:
                HANDLERS[choice]()
            except KeyboardInterrupt:
                print(f"\n  {Fore.LIGHTRED_EX}[!] Abgebrochen.{Style.RESET_ALL}")
                time.sleep(0.6)
        elif choice == "9":
            print_devil()
            pause()
        elif choice in {"0", "exit", "quit", "q"}:
            print(f"  {Fore.LIGHTRED_EX}>> {Fore.WHITE}"
                  f"Bye. Stay in the shadows.{Style.RESET_ALL}\n")
            break
        else:
            print(f"  {Fore.LIGHTRED_EX}[!] Unbekannte Option:"
                  f" {choice}{Style.RESET_ALL}")
            time.sleep(0.8)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    try:
        matrix_rain(duration=1.4)
        print_main_banner()
        boot_sequence()
        print_devil()
        main_loop()
    except KeyboardInterrupt:
        print(f"\n  {Fore.LIGHTRED_EX}[!] Abgebrochen vom User.{Style.RESET_ALL}")
        sys.exit(0)


if __name__ == "__main__":
    main()
