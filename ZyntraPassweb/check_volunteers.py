import psycopg2
conn = psycopg2.connect('postgresql://postgres:Harsha%4020042006@db.qokgtrabcxtxlympbkyb.supabase.co:5432/postgres')
cur = conn.cursor()
cur.execute("SELECT * FROM volunteers")
print("Volunteers:", cur.fetchall())
conn.close()
