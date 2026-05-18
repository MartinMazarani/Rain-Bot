# RAIN BOT

Stylish Python CLI toolkit with a creepy hacker-red theme.

## Intro flow
1. Matrix rain (red)
2. `RAIN BOT` ASCII banner with blood-red gradient
3. Animated boot loading bars
4. **Devil reveal** - top-to-bottom red fade-in:
   - if `logo.png` is present next to `rainbot.py` and Pillow is installed,
     it will be converted to ASCII (brightness 0-9, dark pixels stripped).
   - otherwise: built-in ASCII devil
5. Tools menu

## Tools

| # | Tool | Description |
|---|------|-------------|
| 1 | IP Lookup          | Geo / ISP / ASN via ip-api.com (no API key) |
| 2 | Webhook Sender     | Send messages to Discord webhooks |
| 3 | Port Scanner       | Multi-threaded TCP port scan (common / range / custom) |
| 4 | Hash Generator     | MD5 / SHA1 / SHA256 / SHA512 for strings or files |
| 5 | Password Generator | Cryptographically secure random passwords |
| 9 | Show Devil         | Re-render the devil reveal |
| 0 | Exit               | Leave the bot |

## Install

```bash
pip install -r requirements.txt
```

`colorama`, `pyfiglet`, and `Pillow` are all **optional** - the tool still runs
without them (no PNG -> ASCII devil, no figlet -> built-in banner).

## Logo image

Drop your devil image as `logo.png` next to `rainbot.py`:

```
Rain-Bot/
├── rainbot.py
├── logo.png        <-- your image (PNG / JPG)
└── requirements.txt
```

The image is converted using:

```python
brightness = pixels[x, y]
value = brightness // 26
" " if value < 2 else str(value)
```

## Run

```bash
python rainbot.py
```

## Disclaimer

For educational use and authorized testing of your own systems only.
