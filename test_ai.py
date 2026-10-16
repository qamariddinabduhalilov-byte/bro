"""AI kalitni tekshirish: python test_ai.py   (app.py bilan bir papkada, .env dan o'qiydi)"""
import os, json, urllib.request, urllib.error

def load_env():
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(p):
        for line in open(p, encoding="utf-8-sig"):
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1); os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
load_env()
KEY = os.getenv("GEMINI_KEY", "").strip()
if not KEY:
    KEY = input("GEMINI_KEY topilmadi (.env da yo'q). Kalitni shu yerga qo'ying: ").strip()
print("Kalit boshi:", KEY[:6] + "...  uzunligi:", len(KEY))
body = json.dumps({"contents": [{"role": "user", "parts": [{"text": "Salom, bitta so'z bilan javob ber."}]}]}).encode()
tests = [
    ("Gemini API / gemini-3.5-flash", "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent", {"x-goog-api-key": KEY}),
    ("Gemini API / gemini-flash-latest", "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent", {"x-goog-api-key": KEY}),
    ("Vertex express / gemini-3.5-flash", "https://aiplatform.googleapis.com/v1/publishers/google/models/gemini-3.5-flash:generateContent?key=" + KEY, {}),
]
for name, url, h in tests:
    req = urllib.request.Request(url, body, {"Content-Type": "application/json", **h})
    try:
        r = json.load(urllib.request.urlopen(req, timeout=30))
        txt = r["candidates"][0]["content"]["parts"][0].get("text", "")
        print("✅ ISHLADI:", name, "->", txt.strip()[:60])
    except urllib.error.HTTPError as e:
        print("❌", name, "-> HTTP", e.code, e.read().decode("utf-8", "ignore")[:200].replace("\n", " "))
    except Exception as e:
        print("❌", name, "->", e)
input("\nTugadi. Enter bosing...")
