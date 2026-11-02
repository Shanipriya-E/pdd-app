import psycopg2
conn = psycopg2.connect('postgresql://postgres:Harsha%4020042006@db.qokgtrabcxtxlympbkyb.supabase.co:5432/postgres')
cur = conn.cursor()
cur.execute("SELECT status, count(*) FROM volunteers WHERE event_id = '4117d897-9d7e-4acb-bb34-111620fdb698' GROUP BY status")
print(cur.fetchall())
conn.close()
