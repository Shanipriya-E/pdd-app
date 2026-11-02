import psycopg2
conn = psycopg2.connect('postgresql://postgres:Harsha%4020042006@db.qokgtrabcxtxlympbkyb.supabase.co:5432/postgres')
cur = conn.cursor()
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
tables = cur.fetchall()
print('Tables:', tables)
for t in ['volunteers', 'volunteer_requests']:
    if any(t == row[0] for row in tables):
        cur.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{t}'")
        print(f'{t} columns:', cur.fetchall())
conn.close()
