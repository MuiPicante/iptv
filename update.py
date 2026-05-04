import requests
import re
import os

# 1. Die statische Liste einlesen
with open('static.m3u', 'r', encoding='utf-8') as f:
    m3u_content = f.read()

# 2. Den neuen DMAX Link holen
url = "https://www.canlitv.me/live/dmax-canli-hd/1"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://www.canlitv.me/'
}

dmax_m3u8 = None

try:
    print("Suche nach DMAX Stream...")
    response = requests.get(url, headers=headers)
    
    # Sucht im Quelltext nach dem m3u8 Link
    match = re.search(r'(https://cdn[^\'"]+\.m3u8\?[^\'"]+)', response.text)
    
    if match:
        dmax_m3u8 = match.group(1)
        print(f"Erfolgreich gefunden: {dmax_m3u8}")
    else:
        print("Konnte den Link nicht im Quelltext finden (Evtl. Bot-Schutz).")
except Exception as e:
    print(f"Fehler beim Abrufen: {e}")

# 3. Den DMAX Link zur Liste hinzufügen
if dmax_m3u8:
    m3u_content += f'\n#EXTINF:-1 tvg-name="DMAX" tvg-id="DMAX.tr" tvg-logo="" group-title="BELGESEL",DMAX\n'
    m3u_content += f'{dmax_m3u8}|Referer=https://www.canlitv.me/&User-Agent=Mozilla/5.0\n'

# 4. Die neue index.m3u speichern
with open('index.m3u', 'w', encoding='utf-8') as f:
    f.write(m3u_content)

print("index.m3u wurde erfolgreich aktualisiert!")