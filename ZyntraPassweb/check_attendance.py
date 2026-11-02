import psycopg2
conn = psycopg2.connect('postgresql://postgres:Harsha%4020042006@db.qokgtrabcxtxlympbkyb.supabase.co:5432/postgres')
cur = conn.cursor()
cur.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'attendance_logs'")
print("--- attendance_logs ---")
for row in cur.fetchall(): print(f"{row[0]}: {row[1]}")
conn.close()
