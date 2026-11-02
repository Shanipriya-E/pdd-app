import urllib.request
import json
import ssl

SERVICE_ROLE = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFva2d0cmFiY3h0eGx5bXBia3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4NzM4MzIwNiwiZXhwIjoyMTAyOTU5MjA2fQ.lDo2iSLKm5JArfFwSYKX__3740_sxQHE2m7uCv57_nU'
URL = 'https://qokgtrabcxtxlympbkyb.supabase.co/rest/v1/event_registrations?limit=1'

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(URL, headers={'apikey': SERVICE_ROLE, 'Authorization': 'Bearer ' + SERVICE_ROLE})
with urllib.request.urlopen(req, context=ctx) as response:
    reg_id = json.loads(response.read().decode())[0]['id']

words = ['registered', 'pending', 'joined', 'yes', 'no', 'true', 'false', 'Accept', 'Reject', 'accept', 'reject', 'Approved', 'Rejected', 'Registered']
for status in words:
    try:
        req = urllib.request.Request(
            f'https://qokgtrabcxtxlympbkyb.supabase.co/rest/v1/event_registrations?id=eq.{reg_id}',
            data=json.dumps({"status": status}).encode('utf-8'),
            headers={'apikey': SERVICE_ROLE, 'Authorization': 'Bearer ' + SERVICE_ROLE, 'Content-Type': 'application/json', 'Prefer': 'return=representation'},
            method='PATCH'
        )
        with urllib.request.urlopen(req, context=ctx) as res2:
            print(f"SUCCESS: {status}")
    except Exception as e:
        print(f"FAILED: {status}")
