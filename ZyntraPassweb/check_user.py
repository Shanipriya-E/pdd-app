import psycopg2
conn = psycopg2.connect('postgresql://postgres:Harsha%4020042006@db.qokgtrabcxtxlympbkyb.supabase.co:5432/postgres')
cur = conn.cursor()
cur.execute("SELECT id, full_name, role FROM profiles WHERE full_name = 'ad' OR id = 'fabcf9aa-f406-438e-98ca-65671ea1dd41'")
print(cur.fetchall())
conn.close()
