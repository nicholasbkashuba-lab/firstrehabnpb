import json, os, time, urllib.parse, urllib.request
UA = "FirstRehabSiteBot/1.0 (https://www.firstrehabnpb.com; nicholasbkashuba@gmail.com)"
OK = ("cc by", "cc-by", "cc0", "public domain", "pd")
PLACES = {
 "norton": "Norton Museum of Art West Palm Beach",
 "zoo": "Palm Beach Zoo",
 "manatee-lagoon": "Manatee Lagoon West Palm Beach",
 "grassy-waters": "Grassy Waters Preserve",
 "wpb-waterfront": "West Palm Beach waterfront Intracoastal",
 "ann-norton": "Ann Norton Sculpture Gardens",
 "worth-avenue": "Worth Avenue Palm Beach",
 "whitehall": "Whitehall Flagler Museum",
 "peanut-island": "Peanut Island Florida",
 "ocean-reef": "Singer Island beach",
 "macarthur": "John D. MacArthur Beach State Park",
 "anchorage": "North Palm Beach Florida",
 "frenchmans": "Frenchman's Forest Natural Area",
 "gardens-park": "Palm Beach Gardens Florida park",
 "downtown-pbg": "Palm Beach Gardens Florida",
 "gardens-mall": "The Gardens Mall Palm Beach Gardens",
 "loggerhead": "Loggerhead Marinelife Center",
 "juno-pier": "Juno Beach Pier",
 "juno-dunes": "Juno Dunes Natural Area",
 "lighthouse": "Jupiter Inlet Lighthouse",
 "riverbend": "Riverbend Park Jupiter",
 "carlin": "Carlin Park Jupiter",
 "jupiter-beach": "Jupiter Beach Florida",
 "dubois": "DuBois Park Jupiter",
 "coral-cove": "Coral Cove Park Tequesta",
 "harbourside": "Harbourside Place Jupiter",
 "roger-dean": "Roger Dean Stadium",
 "blowing-rocks": "Blowing Rocks Preserve",
 "jdsp": "Jonathan Dickinson State Park",
 "jdsp-tower": "Hobe Mountain Jonathan Dickinson",
 "loxahatchee": "Loxahatchee River Jupiter",
}
def get(url, binary=False):
    for i in range(4):
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60)
            return r.read() if binary else r.read().decode()
        except Exception as e:
            print("retry", url[:90], e); time.sleep(5 * (i + 1))
    return None
man = {}
os.makedirs("out", exist_ok=True)
for key, q in PLACES.items():
    api = ("https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrnamespace=6&gsrlimit=14"
           "&prop=imageinfo&iiprop=url|extmetadata|size|mime&iiurlwidth=1600&format=json&gsrsearch=" + urllib.parse.quote(q))
    js = get(api); time.sleep(1)
    if not js: continue
    pages = sorted(json.loads(js).get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 99))
    out = []
    for p in pages:
        ii = (p.get("imageinfo") or [{}])[0]
        md = ii.get("extmetadata", {})
        lic = md.get("LicenseShortName", {}).get("value", "")
        if ii.get("mime") != "image/jpeg" or ii.get("width", 0) < 1000 or not lic.lower().startswith(OK): continue
        n = len(out)
        b = get(ii.get("thumburl") or ii["url"], True); time.sleep(1)
        if not b: continue
        fn = f"out/{key}-{n}.jpg"; open(fn, "wb").write(b)
        out.append({"file": fn, "title": p["title"], "page": ii.get("descriptionurl"), "license": lic,
                    "license_url": md.get("LicenseUrl", {}).get("value", ""),
                    "artist": md.get("Artist", {}).get("value", ""), "credit": md.get("Credit", {}).get("value", ""),
                    "desc": md.get("ImageDescription", {}).get("value", "")[:300], "w": ii.get("width"), "h": ii.get("height")})
        if len(out) >= 6: break
    man[key] = out
    print(key, len(out))
json.dump(man, open("out/manifest.json", "w"), indent=1)
for name, url in {"blowing-rocks": "https://www.nature.org/en-us/get-involved/how-to-help/places-we-protect/blowing-rocks-preserve/",
                  "jdsp": "https://www.floridastateparks.org/parks-and-trails/jonathan-dickinson-state-park",
                  "jdsp-hike": "https://www.floridastateparks.org/parks-and-trails/jonathan-dickinson-state-park/activities"}.items():
    h = get(url)
    if h: open(f"out/page-{name}.html", "w").write(h)
