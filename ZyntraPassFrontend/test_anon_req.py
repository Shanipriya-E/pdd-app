import urllib.request

URL_BASE = "https://qokgtrabcxtxlympbkyb.supabase.co"
ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFva2d0cmFiY3h0eGx5bXBia3liIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODczODMyMDYsImV4cCI6MjEwMjk1OTIwNn0.hbs5MZ4FiqUoZxDTrGqtMPOjRbbKUupgZOcoeLZa3ME"
userId = "31668f50-8ab6-41fd-9a19-083d8b067051"

req = urllib.request.Request(
    f"{URL_BASE}/rest/v1/event_registrations?attendee_id=eq.{userId}&select=event_id,status",
    headers={
        "apikey": ANON_KEY
    },
    method="GET"
)
try:
    response = urllib.request.urlopen(req)
    print("Success:", response.read().decode('utf-8'))
except Exception as e:
    print("Error:", str(e))
