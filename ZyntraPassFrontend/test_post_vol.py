import urllib.request
import json
import urllib.error

URL_BASE = "https://qokgtrabcxtxlympbkyb.supabase.co"
SERVICE_ROLE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFva2d0cmFiY3h0eGx5bXBia3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4NzM4MzIwNiwiZXhwIjoyMTAyOTU5MjA2fQ.lDo2iSLKm5JArfFwSYKX__3740_sxQHE2m7uCv57_nU"

data = {
    "event_id": "981c206b-d8e5-4d3c-804c-14b0a4db5c7c",
    "user_id": "31668f50-8ab6-41fd-9a19-083d8b067051",
    "status": "pending"
}

req = urllib.request.Request(
    f"{URL_BASE}/rest/v1/volunteers",
    data=json.dumps(data).encode('utf-8'),
    headers={
        "apikey": SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SERVICE_ROLE_KEY}",
        "Content-Type": "application/json"
    },
    method="POST"
)

try:
    response = urllib.request.urlopen(req)
    print("Success:", response.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print("HTTP Error:", e.code)
    print("Error body:", e.read().decode('utf-8'))
except Exception as e:
    print("Error:", str(e))
