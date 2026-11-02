import os
import psycopg2

conn = psycopg2.connect('postgresql://postgres:Harsha%4020042006@db.qokgtrabcxtxlympbkyb.supabase.co:5432/postgres')
cur = conn.cursor()

organizer_id = 'fabcf9aa-f406-438e-98ca-65671ea1dd41'
cur.execute(f"SET request.jwt.claim.sub = '{organizer_id}'")
cur.execute("SET request.jwt.claim.role = 'authenticated'")
cur.execute("SET role authenticated")

cur.execute("SELECT id, event_id, user_id, status FROM volunteers")
print("As Organizer:", cur.fetchall())

conn.close()
