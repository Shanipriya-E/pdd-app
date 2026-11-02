import psycopg2
conn = psycopg2.connect('postgresql://postgres:Harsha%4020042006@db.qokgtrabcxtxlympbkyb.supabase.co:5432/postgres')
cur = conn.cursor()
cur.execute("SELECT organizer_id, title FROM events WHERE id = '4117d897-9d7e-4acb-bb34-111620fdb698'")
print(cur.fetchall())
conn.close()
