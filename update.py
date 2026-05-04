import os
from playwright.sync_api import sync_playwright

# 1. Die statische Liste einlesen
with open('static.m3u', 'r', encoding='utf-8') as f:
    m3u_content = f.read()

dmax_m3u8 = None

# 2. Einen echten Browser (unsichtbar) starten
with sync_playwright() as p:
    print("Starte unsichtbaren Chrome Browser...")
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    )

    # 3. Wir klinken uns in den Netzwerkverkehr ein
    def intercept_request(request):
        global dmax_m3u8
        # Wir suchen nach der URL, die .m3u8 und ein Token (tkn=) enthält
        if ".m3u8" in request.url and "tkn=" in request.url:
            dmax_m3u8 = request.url

    page.on("request", intercept_request)

    print("Rufe DMAX Seite auf...")
    try:
        # Seite aufrufen und kurz warten, bis die JS-Skripte den Player laden
        page.goto("https://www.canlitv.me/live/dmax-canli-hd/1", timeout=30000)
        page.wait_for_timeout(8000) # 8 Sekunden warten
    except Exception as e:
        print(f"Info beim Laden: {e}")

    browser.close()

# 4. Prüfen, ob wir was gefangen haben und eintragen
if dmax_m3u8:
    print(f"BINGO! Link gefangen: {dmax_m3u8}")
    m3u_content += f'\n#EXTINF:-1 tvg-name="DMAX" tvg-id="DMAX.tr" tvg-logo="" group-title="BELGESEL",DMAX\n'
    m3u_content += f'{dmax_m3u8}|Referer=https://www.canlitv.me/&User-Agent=Mozilla/5.0\n'
else:
    print("Konnte den Stream-Link nicht abfangen. Cloudflare blockt den Browser.")

# 5. Die neue index.m3u speichern
with open('index.m3u', 'w', encoding='utf-8') as f:
    f.write(m3u_content)

print("Skript beendet.")