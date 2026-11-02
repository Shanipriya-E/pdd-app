import psycopg2
conn = psycopg2.connect('postgresql://postgres:Harsha%4020042006@db.qokgtrabcxtxlympbkyb.supabase.co:5432/postgres')
cur = conn.cursor()
cur.execute("SELECT status, count(*) FROM volunteers WHERE event_id = 'f2749c9e-2222-4943-86e2-06b75c9c66da' GROUP BY status")
print(cur.fetchall())
conn.close()
