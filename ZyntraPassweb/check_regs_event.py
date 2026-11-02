import psycopg2
conn = psycopg2.connect('postgresql://postgres:Harsha%4020042006@db.qokgtrabcxtxlympbkyb.supabase.co:5432/postgres')
cur = conn.cursor()
cur.execute("SELECT event_id, status, count(*) FROM event_registrations GROUP BY event_id, status")
print(cur.fetchall())
conn.close()
