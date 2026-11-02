import psycopg2
conn = psycopg2.connect('postgresql://postgres:Harsha%4020042006@db.qokgtrabcxtxlympbkyb.supabase.co:5432/postgres')
cur = conn.cursor()

cur.execute("""
CREATE POLICY "Anyone can read approved volunteers"
ON volunteers FOR SELECT
USING (status = 'approved');
""")
conn.commit()
print("Policy added.")
conn.close()
