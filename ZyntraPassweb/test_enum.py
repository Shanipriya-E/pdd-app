import urllib.request
import json
import ssl

SERVICE_ROLE = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFva2d0cmFiY3h0eGx5bXBia3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4NzM4MzIwNiwiZXhwIjoyMTAyOTU5MjA2fQ.lDo2iSLKm5JArfFwSYKX__3740_sxQHE2m7uCv57_nU'
URL = 'https://qokgtrabcxtxlympbkyb.supabase.co/rest/v1/event_registrations?limit=1'

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(URL, headers={
    'apikey': SERVICE_ROLE,
    'Authorization': 'Bearer ' + SERVICE_ROLE
})

try:
    with urllib.request.urlopen(req, context=ctx) as response:
        data = json.loads(response.read().decode())
        if len(data) > 0:
            reg_id = data[0]['id']
            print("Found registration:", reg_id, "Current status:", data[0]['status'])
            
            # Try to update to 'accepted'
            update_req = urllib.request.Request(
                f'https://qokgtrabcxtxlympbkyb.supabase.co/rest/v1/event_registrations?id=eq.{reg_id}',
                data=json.dumps({"status": "accepted"}).encode('utf-8'),
                headers={
                    'apikey': SERVICE_ROLE,
                    'Authorization': 'Bearer ' + SERVICE_ROLE,
                    'Content-Type': 'application/json',
                    'Prefer': 'return=representation'
                },
                method='PATCH'
            )
            try:
                with urllib.request.urlopen(update_req, context=ctx) as res2:
                    print("Updated to 'accepted':", res2.read().decode())
            except urllib.error.HTTPError as e:
                print("Failed 'accepted':", e.read().decode())
                
            # Try to update to 'approved'
            update_req2 = urllib.request.Request(
                f'https://qokgtrabcxtxlympbkyb.supabase.co/rest/v1/event_registrations?id=eq.{reg_id}',
                data=json.dumps({"status": "approved"}).encode('utf-8'),
                headers={
                    'apikey': SERVICE_ROLE,
                    'Authorization': 'Bearer ' + SERVICE_ROLE,
                    'Content-Type': 'application/json',
                    'Prefer': 'return=representation'
                },
                method='PATCH'
            )
            try:
                with urllib.request.urlopen(update_req2, context=ctx) as res3:
                    print("Updated to 'approved':", res3.read().decode())
            except urllib.error.HTTPError as e:
                print("Failed 'approved':", e.read().decode())
        else:
            print("No registrations found.")
except Exception as e:
    print("Error:", e)
