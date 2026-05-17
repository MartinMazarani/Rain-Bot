#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAIN BOT
--------
Stylisches CLI-Tool im Cyber-/Hacker-Look mit:
  * ASCII-Art Banner (Gradient gefaerbt)
  * Animierter Loading-Bar beim Start
  * Matrix-Style "Rain"-Intro
  * Interaktives Hauptmenue
"""

from __future__ import annotations

import os
import platform
import random
import shutil
import socket
import sys
import time
from datetime import datetime
from typing import List

# colorama ist optional - Fallback auf "leere" Farben wenn nicht installiert
try:
    from colorama import Fore, Style, init as colorama_init
    colorama_init(autoreset=True)
except ImportError:
    class _Dummy:
        def __getattr__(self, _): return ""
    Fore = Style = _Dummy()  # type: ignore

# pyfiglet ist optional - wir haben ein eingebautes Banner als Fallback
try:
    import pyfiglet  # type: ignore
    HAS_PYFIGLET = True
except ImportError:
    HAS_PYFIGLET = False


# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

AUTHOR = "proxytq"
VERSION = "1.0.0"
TOOL_NAME = "RAIN BOT"

# Cyan -> Blau -> Magenta Gradient (typischer Hacker-Look)
GRADIENT = [
    Fore.CYAN,
    Fore.LIGHTCYAN_EX,
    Fore.LIGHTBLUE_EX,
    Fore.BLUE,
    Fore.LIGHTMAGENTA_EX,
    Fore.MAGENTA,
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def term_size() -> tuple[int, int]:
    size = shutil.get_terminal_size(fallback=(100, 30))
    return size.columns, size.lines


def center(text: str, width: int | None = None) -> str:
    cols = width or term_size()[0]
    return "\n".join(line.center(cols) for line in text.splitlines())


def gradient_text(text: str, colors: List[str] = GRADIENT) -> str:
    """Faerbt jede Zeile mit einer Farbe aus dem Gradient."""
    lines = text.splitlines()
    out = []
    for i, line in enumerate(lines):
        color = colors[i % len(colors)]
        out.append(f"{color}{line}{Style.RESET_ALL}")
    return "\n".join(out)


# ---------------------------------------------------------------------------
# Matrix Rain Intro
# ---------------------------------------------------------------------------

def matrix_rain(duration: float = 1.6) -> None:
    """Kurzer Matrix-Code-Regen oben im Terminal."""
    cols, rows = term_size()
    rows = min(rows, 18)
    charset = "01abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ#@$%&*+="
    end = time.time() + duration
    clear()
    while time.time() < end:
        line = "".join(
            random.choice(charset) if random.random() > 0.25 else " "
            for _ in range(cols)
        )
        # zufaelliger Gruen-Ton fuer Matrix-Feeling
        shade = random.choice([Fore.GREEN, Fore.LIGHTGREEN_EX, Fore.GREEN])
        print(f"{shade}{line}{Style.RESET_ALL}")
        time.sleep(0.04)
    clear()


# ---------------------------------------------------------------------------
# Banner
# ---------------------------------------------------------------------------

# Eingebautes ASCII-Banner als Fallback wenn pyfiglet nicht installiert ist
BUILTIN_BANNER = r"""
 ______       _      _____ _   _    ______  _____  _____
 | ___ \     (_)    |_   _| \ | |   | ___ \|  _  ||_   _|
 | |_/ /__ _  _ _ __  | | |  \| |   | |_/ /| | | |  | |
 |    // _` || | '_ \ | | | . ` |   | ___ \| | | |  | |
 | |\ \ (_| || | | | || |_| |\  |   | |_/ /\ \_/ /  | |
 \_| \_\__,_||_|_| |_\___/\_| \_/   \____/  \___/   \_/
"""


def render_banner() -> str:
    if HAS_PYFIGLET:
        fig = pyfiglet.figlet_format(TOOL_NAME, font="ansi_shadow")
    else:
        fig = BUILTIN_BANNER
    return gradient_text(fig)


def subtitle() -> str:
    cols = term_size()[0]
    bar = f"{Fore.LIGHTBLACK_EX}{'-' * min(cols - 4, 70)}{Style.RESET_ALL}"
    info = (
        f"{Fore.LIGHTCYAN_EX}>> {Fore.WHITE}Author : {Fore.LIGHTMAGENTA_EX}{AUTHOR}"
        f"   {Fore.WHITE}Version: {Fore.LIGHTMAGENTA_EX}v{VERSION}"
        f"   {Fore.WHITE}Build  : {Fore.LIGHTMAGENTA_EX}{datetime.now():%Y-%m-%d}"
    )
    return f"{center(bar)}\n{center(info)}\n{center(bar)}"


def print_banner() -> None:
    clear()
    cols = term_size()[0]
    print()
    for line in render_banner().splitlines():
        # pyfiglet output ist schon farbig, aber center() bricht ANSI -> safe centern
        plain_len = len(line) - sum(line.count(c) for c in GRADIENT) * len(GRADIENT[0])
        pad = max((cols - len(line)) // 2, 0)
        print(" " * pad + line)
    print()
    print(subtitle())
    print()


# ---------------------------------------------------------------------------
# Loading Bar
# ---------------------------------------------------------------------------

SPINNER = ["|", "/", "-", "\\"]


def loading_bar(
    label: str = "Initializing modules",
    duration: float = 3.5,
    width: int = 42,
) -> None:
    """Animierter Lade-Balken mit Spinner und Prozentanzeige."""
    steps = 100
    delay = duration / steps
    start = time.time()

    for i in range(steps + 1):
        filled = int(width * i / steps)
        empty = width - filled

        # Gradient-Balken
        bar_filled = ""
        for j in range(filled):
            color = GRADIENT[j * len(GRADIENT) // max(width, 1) % len(GRADIENT)]
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
        ("Loading core ........", 1.2),
        ("Connecting sockets ..", 1.0),
        ("Decrypting modules ..", 1.4),
        ("Spawning workers ....", 0.9),
        ("Finalizing ..........", 0.7),
    ]
    print()
    for label, dur in tasks:
        loading_bar(label=label, duration=dur, width=38)
    print(f"\n  {Fore.LIGHTGREEN_EX}[OK]{Style.RESET_ALL} "
          f"{Fore.WHITE}All systems online.{Style.RESET_ALL}\n")
    time.sleep(0.6)


# ---------------------------------------------------------------------------
# System Info
# ---------------------------------------------------------------------------

def system_info() -> None:
    try:
        host = socket.gethostname()
        ip = socket.gethostbyname(host)
    except Exception:
        host, ip = "unknown", "0.0.0.0"

    rows = [
        ("OS",       f"{platform.system()} {platform.release()}"),
        ("Arch",     platform.machine()),
        ("Python",   platform.python_version()),
        ("Host",     host),
        ("IP",       ip),
        ("CWD",      os.getcwd()),
        ("Time",     datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    ]
    print(f"  {Fore.LIGHTMAGENTA_EX}>> {Fore.WHITE}SYSTEM INFO{Style.RESET_ALL}")
    print(f"  {Fore.LIGHTBLACK_EX}{'-' * 50}{Style.RESET_ALL}")
    for k, v in rows:
        print(f"  {Fore.LIGHTCYAN_EX}{k:<8}{Style.RESET_ALL} "
              f"{Fore.LIGHTBLACK_EX}:{Style.RESET_ALL} "
              f"{Fore.WHITE}{v}{Style.RESET_ALL}")
    print()


# ---------------------------------------------------------------------------
# Menu
# ---------------------------------------------------------------------------

MENU_ITEMS = [
    ("1", "System Info",        "Zeigt OS / Host / IP Infos"),
    ("2", "Matrix Rain",        "Spielt die Rain-Animation ab"),
    ("3", "Re-run Loading Bar", "Zeigt die Boot-Sequenz nochmal"),
    ("4", "Banner",             "Banner neu rendern"),
    ("0", "Exit",               "Tool beenden"),
]


def print_menu() -> None:
    print(f"  {Fore.LIGHTMAGENTA_EX}>> {Fore.WHITE}MENU{Style.RESET_ALL}")
    print(f"  {Fore.LIGHTBLACK_EX}{'-' * 50}{Style.RESET_ALL}")
    for key, name, desc in MENU_ITEMS:
        print(
            f"  {Fore.LIGHTCYAN_EX}[{key}]{Style.RESET_ALL} "
            f"{Fore.WHITE}{name:<22}{Style.RESET_ALL}"
            f"{Fore.LIGHTBLACK_EX}{desc}{Style.RESET_ALL}"
        )
    print()


def prompt() -> str:
    return input(
        f"  {Fore.LIGHTMAGENTA_EX}root@rainbot{Fore.WHITE}:"
        f"{Fore.LIGHTCYAN_EX}~{Fore.WHITE}$ {Style.RESET_ALL}"
    ).strip()


def main_loop() -> None:
    while True:
        print_menu()
        choice = prompt()
        print()
        if choice == "1":
            system_info()
        elif choice == "2":
            matrix_rain(duration=2.5)
            print_banner()
        elif choice == "3":
            boot_sequence()
        elif choice == "4":
            print_banner()
        elif choice in {"0", "exit", "quit", "q"}:
            print(f"  {Fore.LIGHTMAGENTA_EX}>> {Fore.WHITE}"
                  f"Bye! Stay safe out there.{Style.RESET_ALL}\n")
            break
        else:
            print(f"  {Fore.LIGHTRED_EX}[!] Unbekannte Option:"
                  f" {choice}{Style.RESET_ALL}\n")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    try:
        matrix_rain(duration=1.4)
        print_banner()
        boot_sequence()
        main_loop()
    except KeyboardInterrupt:
        print(f"\n  {Fore.LIGHTRED_EX}[!] Abgebrochen vom User.{Style.RESET_ALL}")
        sys.exit(0)


if __name__ == "__main__":
    main()
