import urllib.request
import json

URL_BASE = "https://qokgtrabcxtxlympbkyb.supabase.co"
SERVICE_ROLE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFva2d0cmFiY3h0eGx5bXBia3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4NzM4MzIwNiwiZXhwIjoyMTAyOTU5MjA2fQ.lDo2iSLKm5JArfFwSYKX__3740_sxQHE2m7uCv57_nU"

req = urllib.request.Request(
    f"{URL_BASE}/rest/v1/event_registrations",
    headers={
        "apikey": SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SERVICE_ROLE_KEY}"
    },
    method="GET"
)
try:
    response = urllib.request.urlopen(req)
    print("Success:", response.read().decode('utf-8'))
except Exception as e:
    print("Error:", str(e))
