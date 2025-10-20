import os, json, time, requests

def fetch_groq(key: str|None):
    url = "https://api.groq.com/openai/v1/models"
    hdr = {"Authorization": f"Bearer {key}"} if key else {}
    r = requests.get(url, headers=hdr, timeout=30)
    r.raise_for_status()
    data = r.json()
    out = []
    for m in (data.get("data") or []):
        name = m.get("id") or m.get("name")
        if name:
            out.append(str(name))
    pref = ["llama-3.3-70b-versatile","llama-3.1-8b-instant"]
    out = sorted(set(out), key=lambda x: (0 if x in pref else 1, x))
    return out

def fetch_gemini(key: str|None):
    base = "https://generativelanguage.googleapis.com/v1/models"
    url = f"{base}?key={key}" if key else base
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    data = r.json()
    out = []
    for m in (data.get("models") or []):
        name = m.get("name")
        if name:
            out.append(name.split("/")[-1])
    pref = ["gemini-1.5-flash","gemini-1.5-pro"]
    out = sorted(set(out), key=lambda x: (0 if x in pref else 1, x))
    return out

def main():
    groq_key = os.getenv("GROQ_API_KEY", "")
    gem_key  = os.getenv("GEMINI_API_KEY", "")

    try:
        groq = fetch_groq(groq_key)
    except Exception:
        groq = ["llama-3.3-70b-versatile","llama-3.1-8b-instant"]

    try:
        gemini = fetch_gemini(gem_key)
    except Exception:
        gemini = ["gemini-1.5-flash","gemini-1.5-pro"]

    payload = {
        "groq": groq,
        "gemini": gemini,
        "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    with open("models.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
