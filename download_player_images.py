import os
import json
import urllib.request
import urllib.parse

players_wiki = {
    "Naman Dhir": "Naman_Dhir",
    "Shashank Singh": "Shashank_Singh_(cricketer)",
    "Tim David": "Tim_David",
    "Namboori Tilak Varma": "Tilak_Varma",
    "Jos Buttler": "Jos_Buttler",
    "Rishabh Pant": "Rishabh_Pant",
    "Matthew Wade": "Matthew_Wade",
    "Shreyas Iyer": "Shreyas_Iyer",
    "Rajat Patidar": "Rajat_Patidar",
    "Tristan Stubbs": "Tristan_Stubbs",
    "Sunil Narine": "Sunil_Narine",
    "Jasprit Bumrah": "Jasprit_Bumrah",
    "Shaheen Afridi": "Shaheen_Afridi",
    "Faheem Ashraf": "Faheem_Ashraf",
    "Riley Meredith": "Riley_Meredith",
    "Haris Rauf": "Haris_Rauf",
    "Alzarri Joseph": "Alzarri_Joseph",
    "Shadab Khan": "Shadab_Khan",
    "Xavier Bartlett": "Xavier_Bartlett",
    "Axar Patel": "Axar_Patel",
    "Virat Kohli": "Virat_Kohli",
    "Quinton de Kock": "Quinton_de_Kock",
    "Rovman Powell": "Rovman_Powell",
    "Harpreet Brar": "Harpreet_Brar"
}

headers = {
    "User-Agent": "SupeRRSelectorApp/1.0 (educational sports analytics project; contact@superrselector.org)"
}

out_dirs = [
    os.path.join("web", "public", "players"),
    os.path.join("web", "players")
]

downloaded = {}

for name, wiki_slug in players_wiki.items():
    safe_filename = name.lower().replace(" ", "_").replace("namboori_", "") + ".jpg"
    api_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{wiki_slug}"
    
    img_url = None
    try:
        req = urllib.request.Request(api_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            if "thumbnail" in data and "source" in data["thumbnail"]:
                img_url = data["thumbnail"]["source"]
            elif "originalimage" in data and "source" in data["originalimage"]:
                img_url = data["originalimage"]["source"]
    except Exception as e:
        print(f"Error fetching metadata for {name}: {e}")

    if not img_url:
        # Fallback to direct search or placeholder
        print(f"No direct thumbnail for {name}, using fallback search")
        try:
            search_api = f"https://en.wikipedia.org/w/api.php?action=query&titles={wiki_slug}&prop=pageimages&format=json&pithumbsize=400"
            req = urllib.request.Request(search_api, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                pages = data.get("query", {}).get("pages", {})
                for p_id, p_info in pages.items():
                    if "thumbnail" in p_info:
                        img_url = p_info["thumbnail"]["source"]
                        break
        except Exception as e:
            print(f"Fallback search failed for {name}: {e}")

    if img_url:
        print(f"Downloading image for {name} from {img_url}...")
        try:
            req = urllib.request.Request(img_url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                content = resp.read()
                for d in out_dirs:
                    dest = os.path.join(d, safe_filename)
                    with open(dest, "wb") as f:
                        f.write(content)
            downloaded[name] = f"players/{safe_filename}"
            print(f"Successfully saved {safe_filename}!")
        except Exception as e:
            print(f"Failed to download image bytes for {name}: {e}")
    else:
        print(f"Could not find image for {name}")

print(f"\nTotal downloaded: {len(downloaded)} / {len(players_wiki)}")
with open(os.path.join("web", "data", "downloaded_images.json"), "w") as f:
    json.dump(downloaded, f, indent=2)
