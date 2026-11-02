import psycopg2
conn = psycopg2.connect('postgresql://postgres:Harsha%4020042006@db.qokgtrabcxtxlympbkyb.supabase.co:5432/postgres')
cur = conn.cursor()
cur.execute("SELECT policyname, cmd, qual, with_check FROM pg_policies WHERE tablename = 'objects' AND schemaname = 'storage'")
for row in cur.fetchall(): print(row)
conn.close()
