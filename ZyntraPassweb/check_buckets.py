import psycopg2
conn = psycopg2.connect('postgresql://postgres:Harsha%4020042006@db.qokgtrabcxtxlympbkyb.supabase.co:5432/postgres')
cur = conn.cursor()
cur.execute("SELECT id, name, public FROM storage.buckets")
print("--- storage.buckets ---")
for row in cur.fetchall(): print(row)
conn.close()
