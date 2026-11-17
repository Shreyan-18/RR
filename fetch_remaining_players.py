import urllib.request
import urllib.parse
import json
import re
import os
import time

remaining = {
    "Naman Dhir": "Naman Dhir Mumbai Indians",
    "Shashank Singh": "Shashank Singh Punjab Kings cricketer",
    "Tim David": "Tim David Australia cricket",
    "Rajat Patidar": "Rajat Patidar RCB cricketer",
    "Tristan Stubbs": "Tristan Stubbs South Africa cricket",
    "Faheem Ashraf": "Faheem Ashraf Pakistan cricket",
    "Riley Meredith": "Riley Meredith Australia cricket",
    "Alzarri Joseph": "Alzarri Joseph West Indies cricket",
    "Xavier Bartlett": "Xavier Bartlett Australia cricket",
    "Rovman Powell": "Rovman Powell West Indies cricket",
    "Harpreet Brar": "Harpreet Brar Punjab Kings cricketer"
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

out_dirs = [
    os.path.join("web", "public", "players"),
    os.path.join("web", "players")
]

for name, query in remaining.items():
    safe_name = name.lower().replace(" ", "_") + ".jpg"
    dest1 = os.path.join("web", "players", safe_name)
    if os.path.exists(dest1) and os.path.getsize(dest1) > 5000:
        print(f"{name} already exists.")
        continue
    
    # Try searching Bing or Wikimedia
    q = urllib.parse.quote(query)
    search_url = f"https://www.bing.com/images/search?q={q}&form=HDRSC2&first=1"
    
    img_url = None
    try:
        req = urllib.request.Request(search_url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            # Extract murl
            murls = re.findall(r'murl&quot;:&quot;(https?://[^&]+?\.(?:jpg|jpeg|png))&quot;', html)
            if murls:
                for cand in murls:
                    if not any(bad in cand.lower() for bad in ['logo', 'icon', 'banner', 'svg', 'watermark']):
                        img_url = cand
                        break
    except Exception as e:
        print(f"Error searching for {name}: {e}")

    if img_url:
        print(f"Downloading {name} from {img_url[:70]}...")
        try:
            img_req = urllib.request.Request(img_url, headers=headers)
            with urllib.request.urlopen(img_req, timeout=10) as img_resp:
                data = img_resp.read()
                if len(data) > 5000:
                    for d in out_dirs:
                        with open(os.path.join(d, safe_name), 'wb') as f:
                            f.write(data)
                    print(f"Successfully saved {safe_name} ({len(data)} bytes)!")
                else:
                    print(f"Image too small ({len(data)} bytes) for {name}")
        except Exception as e:
            print(f"Failed to download image for {name}: {e}")
    else:
        print(f"No image candidate found for {name}")
    time.sleep(1)

print("Done checking all players!")
