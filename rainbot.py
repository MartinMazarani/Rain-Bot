#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAIN BOT - hacker CLI toolkit
-----------------------------
* matrix rain intro
* RAIN BOT banner with blood-red gradient
* boot sequence with animated loading bars
* red devil ASCII (doxbin / metal style)
* 5 real tools
"""

from __future__ import annotations

import hashlib
import json
import os
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
# Enable ANSI on Windows
# ---------------------------------------------------------------------------

if os.name == "nt":
    # turn on virtual terminal processing so 256-color codes work
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except Exception:
        pass
    try:
        from colorama import just_fix_windows_console  # type: ignore
        just_fix_windows_console()
    except ImportError:
        try:
            from colorama import init as _ci  # type: ignore
            _ci()
        except ImportError:
            pass

# pyfiglet is optional - we ship a builtin banner as fallback
try:
    import pyfiglet  # type: ignore
    HAS_PYFIGLET = True
except ImportError:
    HAS_PYFIGLET = False

# Pillow is optional - if available we render logo.png as ASCII
try:
    from PIL import Image  # type: ignore
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


# ---------------------------------------------------------------------------
# Creepy hacker-red color palette (ANSI 256)
# ---------------------------------------------------------------------------

class C:
    R       = "\033[0m"           # reset
    B       = "\033[1m"           # bold
    DIM     = "\033[2m"

    # red gradient: dark blood -> bright red
    DARK    = "\033[38;5;52m"     # very dark blood
    BLOOD   = "\033[38;5;88m"     # blood
    RED     = "\033[38;5;124m"    # red
    HOT     = "\033[38;5;160m"    # hot red
    BRIGHT  = "\033[38;5;196m"    # bright red

    # accents
    GREY    = "\033[38;5;240m"
    WHITE   = "\033[38;5;255m"
    BONE    = "\033[38;5;230m"
    GREEN   = "\033[38;5;46m"


# blood-wave gradient for banner / loading bar
RED_GRADIENT = [C.DARK, C.BLOOD, C.RED, C.HOT, C.BRIGHT, C.HOT, C.RED, C.BLOOD]
DEVIL_GRADIENT = [C.BRIGHT, C.HOT, C.RED, C.HOT, C.BRIGHT, C.HOT, C.RED, C.BLOOD, C.DARK]


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

AUTHOR = "proxytq"
VERSION = "1.2.0"
TOOL_NAME = "RAIN BOT"


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


def gradient_text(text: str, palette: List[str] = RED_GRADIENT) -> str:
    out = []
    for i, line in enumerate(text.splitlines()):
        out.append(f"{palette[i % len(palette)]}{line}{C.R}")
    return "\n".join(out)


def section(label: str) -> None:
    cols = term_size()[0]
    bar = "-" * min(cols - 4, 60)
    print(f"  {C.GREY}{bar}{C.R}")
    print(f"  {C.BRIGHT}>> {C.WHITE}{label}{C.R}")
    print(f"  {C.GREY}{bar}{C.R}")


def pause() -> None:
    input(f"\n  {C.GREY}[ENTER] back to menu...{C.R}")


# ---------------------------------------------------------------------------
# Matrix Rain (red, not green - to match the theme)
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
        shade = random.choice([C.DARK, C.BLOOD, C.RED, C.HOT, C.BRIGHT])
        print(f"{shade}{line}{C.R}")
        time.sleep(0.04)
    clear()


# ---------------------------------------------------------------------------
# RAIN BOT main banner
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
        # ANSI escapes don't take visual space, but when pyfiglet is off
        # the line has no escapes; either way center on raw length.
        plain = line
        for code in RED_GRADIENT + [C.R]:
            plain = plain.replace(code, "")
        pad = max((cols - len(plain)) // 2, 0)
        print(" " * pad + line)

    bar = f"{C.GREY}{'-' * min(cols - 4, 70)}{C.R}"
    info = (
        f"{C.BRIGHT}>> {C.WHITE}author : {C.HOT}{AUTHOR}"
        f"   {C.WHITE}version: {C.HOT}v{VERSION}"
        f"   {C.WHITE}build  : {C.HOT}{datetime.now():%Y-%m-%d}"
    )
    print()
    print(center_block(bar))
    print(center_block(info))
    print(center_block(bar))
    print()


# ---------------------------------------------------------------------------
# Devil ASCII (red, doxbin / hardcore style)
# ---------------------------------------------------------------------------

DEVIL_ART = r'''
        \\.                                                  .//
         \\\\.                                             ./////
          \\\\\\.                                       .///////
           \\\\\\\\.                                  .////////
            \\\\\\\\\\.                            ./////////
             \\\\\\\\\\\\.                       ./////////
              \\\\\\\\\\\\\\.                  ./////////
               \\\\\\\\\\\\\\\\.            .///////////
                \\\\\\\\\\\\\\\\\\\.    .//////////////
                 \\\\\\\\\\\\\\\\\\\\\\////////////////
                  \\\\\\__________________________////
                   \\__/                          \__/
                  /  __                            __  \
                 /  /  \                          /  \  \
                | |    |    >>>>      <<<<       |    | |
                 \  \__/                          \__/  /
                  \                                    /
                   |       \\                //       |
                    \       \\\\\\\\\\\\\\\\//       /
                     \       \\\\\\\\\\\\\\//       /
                      \       \\__________//       /
                       \       \  V V V  /        /
                        \       \  ^^^  /        /
                         \       \_____/        /
                          \                    /
                           \__________________/
                              \\\\\\______/////
                               \\\\\\\__////
                                 \\\V////
                                  \\V//
                                   \V/
                                    V
'''


def render_logo_ascii(path: str, width: int = 120, height: int = 60) -> List[str] | None:
    """
    Convert an image (PNG/JPG) to ASCII lines using brightness 0-9.
    Mirrors the snippet:
        value = brightness // 26
        if value < 2: space else: str(value)
    Returns the list of ASCII lines, or None if Pillow / file is missing.
    """
    if not HAS_PIL:
        return None
    try:
        img = Image.open(path).convert("L")
    except (FileNotFoundError, OSError):
        return None

    img = img.resize((width, height))
    pixels = img.load()

    lines: List[str] = []
    for y in range(img.height):
        line_chars = []
        for x in range(img.width):
            brightness = pixels[x, y]
            value = brightness // 26     # 0-9 (255//26 = 9)
            if value < 2:
                line_chars.append(" ")
            else:
                line_chars.append(str(value))
        lines.append("".join(line_chars))
    return lines


def _logo_path() -> str:
    """Look for logo.png next to this script."""
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "logo.png")


def print_devil() -> None:
    """
    Render the devil banner with a row-by-row red top-to-bottom reveal.
    Tries logo.png first (via Pillow), falls back to the ASCII devil art.
    """
    clear()
    cols = term_size()[0]

    # Try the image first
    lines: List[str] | None = None
    if HAS_PIL:
        # Scale ASCII width to terminal but cap at 120
        target_w = min(cols - 4, 120)
        # rough 2:1 char aspect ratio -> halve height
        target_h = max(20, int(target_w * 0.5))
        lines = render_logo_ascii(_logo_path(), width=target_w, height=target_h)

    if lines is None:
        # Fallback: ASCII devil art
        lines = DEVIL_ART.splitlines()

    print()
    n = len(lines)
    for i, line in enumerate(lines):
        # gradient mapped to vertical position so the reveal goes
        # dark (top) -> bright (middle) -> dark (bottom)
        rel = i / max(n - 1, 1)
        if rel < 0.20:
            color = C.DARK
        elif rel < 0.40:
            color = C.BLOOD
        elif rel < 0.60:
            color = C.RED
        elif rel < 0.80:
            color = C.HOT
        else:
            color = C.BRIGHT

        pad = max((cols - len(line)) // 2, 0)
        sys.stdout.write(" " * pad + f"{C.B}{color}{line}{C.R}\n")
        sys.stdout.flush()
        # speed up for tall images so the reveal stays snappy
        time.sleep(0.025 if n > 30 else 0.04)

    print()
    sub = (
        f"{C.HOT}>> {C.BRIGHT}{AUTHOR}{C.HOT} :: "
        f"{C.WHITE}all systems compromised{C.R}"
    )
    print(center_block(sub))
    tag = f"{C.DARK}-- welcome to hell --{C.R}"
    print(center_block(tag))
    print()
    time.sleep(1.0)


# ---------------------------------------------------------------------------
# Loading bar (red gradient, no more pride colors)
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
            color = RED_GRADIENT[(j * len(RED_GRADIENT) // max(width, 1)) % len(RED_GRADIENT)]
            bar_filled += f"{color}#{C.R}"
        bar_empty = f"{C.GREY}{'-' * empty}{C.R}"

        spin = SPINNER[i % len(SPINNER)]
        elapsed = time.time() - start
        line = (
            f"  {C.BRIGHT}[{spin}]{C.R} "
            f"{C.WHITE}{label:<22}{C.R} "
            f"{C.GREY}[{C.R}"
            f"{bar_filled}{bar_empty}"
            f"{C.GREY}]{C.R} "
            f"{C.HOT}{i:3d}%{C.R} "
            f"{C.GREY}({elapsed:4.1f}s){C.R}"
        )
        sys.stdout.write("\r" + line)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def boot_sequence() -> None:
    tasks = [
        ("loading core .......", 1.0),
        ("opening sockets ....", 0.9),
        ("decrypting modules .", 1.2),
        ("spawning workers ...", 0.8),
        ("summoning daemons ..", 1.0),
        ("finalizing .........", 0.6),
    ]
    print()
    for label, dur in tasks:
        loading_bar(label, dur)
    print(f"\n  {C.GREEN}[OK]{C.R} {C.WHITE}all systems online.{C.R}\n")
    time.sleep(0.5)


# ---------------------------------------------------------------------------
# Tool 1: IP Lookup
# ---------------------------------------------------------------------------

def tool_ip_lookup() -> None:
    section("IP LOOKUP")
    target = input(
        f"  {C.HOT}IP / domain "
        f"{C.GREY}(empty = your own IP){C.WHITE}: {C.R}"
    ).strip()
    url = f"http://ip-api.com/json/{urllib.parse.quote(target)}" if target else "http://ip-api.com/json/"
    try:
        with urllib.request.urlopen(url, timeout=8) as r:
            data = json.loads(r.read().decode())
    except (urllib.error.URLError, socket.timeout) as e:
        print(f"  {C.BRIGHT}[!] error: {e}{C.R}")
        return pause()

    if data.get("status") != "success":
        print(f"  {C.BRIGHT}[!] {data.get('message', 'unknown error')}{C.R}")
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
        print(f"  {C.HOT}{label:<9}{C.R} "
              f"{C.GREY}:{C.R} "
              f"{C.WHITE}{val}{C.R}")
    pause()


# ---------------------------------------------------------------------------
# Tool 2: Webhook Sender (Discord)
# ---------------------------------------------------------------------------

def tool_webhook() -> None:
    section("WEBHOOK SENDER")
    print(f"  {C.GREY}send a message to a Discord webhook.{C.R}\n")
    url = input(f"  {C.HOT}webhook URL{C.WHITE}: {C.R}").strip()
    if not url.startswith(("https://discord.com/api/webhooks/",
                           "https://discordapp.com/api/webhooks/")):
        print(f"  {C.BRIGHT}[!] invalid Discord webhook URL.{C.R}")
        return pause()

    username = input(f"  {C.HOT}username   {C.GREY}(optional){C.WHITE}: {C.R}").strip()
    content  = input(f"  {C.HOT}message    {C.WHITE}: {C.R}").strip()
    try:
        count = int(input(f"  {C.HOT}send count {C.GREY}(default 1){C.WHITE}: {C.R}") or "1")
    except ValueError:
        count = 1
    count = max(1, min(count, 50))  # safety cap

    if not content:
        print(f"  {C.BRIGHT}[!] empty message - aborted.{C.R}")
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
            headers={"Content-Type": "application/json", "User-Agent": "RainBot/1.2"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=8) as r:
                if 200 <= r.status < 300:
                    print(f"  {C.GREEN}[OK]{C.R} #{i} sent ({r.status})")
                    ok += 1
                else:
                    print(f"  {C.BRIGHT}[!]{C.R} #{i} status {r.status}")
                    fail += 1
        except urllib.error.HTTPError as e:
            print(f"  {C.BRIGHT}[!]{C.R} #{i} HTTP {e.code}: {e.reason}")
            fail += 1
        except Exception as e:
            print(f"  {C.BRIGHT}[!]{C.R} #{i} {e}")
            fail += 1
        time.sleep(0.6)  # rate-limit friendly

    print(f"\n  {C.HOT}>> {C.WHITE}done. "
          f"{C.GREEN}{ok} ok{C.WHITE} / "
          f"{C.BRIGHT}{fail} fail{C.R}")
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
    section("PORT SCANNER")
    host = input(f"  {C.HOT}target host/IP{C.WHITE}: {C.R}").strip()
    if not host:
        return
    mode = input(f"  {C.HOT}mode {C.GREY}"
                 f"[1] common  [2] range  [3] custom{C.WHITE}: {C.R}").strip()

    if mode == "2":
        try:
            lo = int(input(f"  {C.HOT}from{C.WHITE}: {C.R}"))
            hi = int(input(f"  {C.HOT}to  {C.WHITE}: {C.R}"))
        except ValueError:
            print(f"  {C.BRIGHT}[!] invalid input{C.R}")
            return pause()
        ports = list(range(max(1, lo), min(65535, hi) + 1))
    elif mode == "3":
        raw = input(f"  {C.HOT}ports (comma separated){C.WHITE}: {C.R}")
        try:
            ports = [int(p) for p in raw.replace(" ", "").split(",") if p]
        except ValueError:
            print(f"  {C.BRIGHT}[!] invalid ports{C.R}")
            return pause()
    else:
        ports = COMMON_PORTS

    try:
        ip = socket.gethostbyname(host)
    except socket.gaierror:
        print(f"  {C.BRIGHT}[!] could not resolve host.{C.R}")
        return pause()

    print(f"\n  {C.HOT}>> {C.WHITE}scanning "
          f"{C.HOT}{host} ({ip}){C.WHITE} - "
          f"{C.HOT}{len(ports)} ports{C.R}\n")

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
                print(f"  {C.GREEN}[+]{C.R} "
                      f"{C.WHITE}{port:>5}/tcp{C.R}  "
                      f"{C.GREY}{svc}{C.R}")

    dur = time.time() - start
    print(f"\n  {C.HOT}>> {C.WHITE}done. "
          f"{C.GREEN}{len(open_ports)} open{C.WHITE} / "
          f"{len(ports)} scanned in "
          f"{C.HOT}{dur:.2f}s{C.R}")
    pause()


# ---------------------------------------------------------------------------
# Tool 4: Hash Generator
# ---------------------------------------------------------------------------

def tool_hash() -> None:
    section("HASH GENERATOR")
    src = input(f"  {C.HOT}source {C.GREY}[1] string  [2] file{C.WHITE}: {C.R}").strip()
    if src == "2":
        path = input(f"  {C.HOT}file path{C.WHITE}: {C.R}").strip()
        if not os.path.isfile(path):
            print(f"  {C.BRIGHT}[!] file not found.{C.R}")
            return pause()
        hashes = {a: hashlib.new(a) for a in ("md5", "sha1", "sha256", "sha512")}
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                for h in hashes.values():
                    h.update(chunk)
        results = {a: h.hexdigest() for a, h in hashes.items()}
        label = path
    else:
        text = input(f"  {C.HOT}text{C.WHITE}: {C.R}")
        data = text.encode()
        results = {
            "md5":    hashlib.md5(data).hexdigest(),
            "sha1":   hashlib.sha1(data).hexdigest(),
            "sha256": hashlib.sha256(data).hexdigest(),
            "sha512": hashlib.sha512(data).hexdigest(),
        }
        label = f'"{text}"' if len(text) <= 40 else f'"{text[:37]}..."'

    print(f"\n  {C.GREY}source: {C.WHITE}{label}{C.R}\n")
    for algo, digest in results.items():
        print(f"  {C.HOT}{algo.upper():<7}{C.R} "
              f"{C.GREY}:{C.R} "
              f"{C.WHITE}{digest}{C.R}")
    pause()


# ---------------------------------------------------------------------------
# Tool 5: Password Generator
# ---------------------------------------------------------------------------

def tool_password() -> None:
    section("PASSWORD GENERATOR")
    try:
        length = int(input(f"  {C.HOT}length   {C.GREY}(default 20){C.WHITE}: {C.R}") or "20")
        count  = int(input(f"  {C.HOT}how many {C.GREY}(default 5){C.WHITE}: {C.R}") or "5")
    except ValueError:
        print(f"  {C.BRIGHT}[!] invalid number{C.R}")
        return pause()

    length = max(4, min(length, 128))
    count  = max(1, min(count, 50))

    use_sym = input(f"  {C.HOT}symbols? {C.GREY}[Y/n]{C.WHITE}: {C.R}").strip().lower() != "n"
    alphabet = string.ascii_letters + string.digits + (string.punctuation if use_sym else "")

    print()
    for i in range(1, count + 1):
        pw = "".join(secrets.choice(alphabet) for _ in range(length))
        # color characters by class
        colored = ""
        for ch in pw:
            if ch.isdigit():
                colored += f"{C.HOT}{ch}"
            elif ch.isalpha():
                colored += f"{C.WHITE}{ch}"
            else:
                colored += f"{C.BRIGHT}{ch}"
        print(f"  {C.GREY}{i:>2}.{C.R} {colored}{C.R}")
    pause()


# ---------------------------------------------------------------------------
# Menu
# ---------------------------------------------------------------------------

MENU_ITEMS = [
    ("1", "IP Lookup",          "geo / ISP / ASN via ip-api"),
    ("2", "Webhook Sender",     "send messages to Discord webhooks"),
    ("3", "Port Scanner",       "multi-threaded TCP port scan"),
    ("4", "Hash Generator",     "MD5 / SHA1 / SHA256 / SHA512"),
    ("5", "Password Generator", "secure random passwords"),
    ("9", "Show Devil",         "render the devil again"),
    ("0", "Exit",               "leave the bot"),
]


def print_menu() -> None:
    print(f"  {C.BRIGHT}>> {C.WHITE}TOOLS{C.R}")
    print(f"  {C.GREY}{'-' * 60}{C.R}")
    for key, name, desc in MENU_ITEMS:
        print(
            f"  {C.HOT}[{key}]{C.R} "
            f"{C.WHITE}{name:<20}{C.R}"
            f"{C.GREY}{desc}{C.R}"
        )
    print()


def prompt() -> str:
    return input(
        f"  {C.BRIGHT}root{C.GREY}@{C.HOT}rainbot"
        f"{C.GREY}:{C.RED}~{C.WHITE}# {C.R}"
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
                print(f"\n  {C.BRIGHT}[!] aborted.{C.R}")
                time.sleep(0.6)
        elif choice == "9":
            print_devil()
            pause()
        elif choice in {"0", "exit", "quit", "q"}:
            print(f"  {C.BRIGHT}>> {C.WHITE}bye. stay in the shadows.{C.R}\n")
            break
        else:
            print(f"  {C.BRIGHT}[!] unknown option: {choice}{C.R}")
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
        print(f"\n  {C.BRIGHT}[!] aborted by user.{C.R}")
        sys.exit(0)


if __name__ == "__main__":
    main()
