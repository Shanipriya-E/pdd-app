import psycopg2
conn = psycopg2.connect('postgresql://postgres:Harsha%4020042006@db.qokgtrabcxtxlympbkyb.supabase.co:5432/postgres')
cur = conn.cursor()
try:
    cur.execute("ALTER TABLE events ADD COLUMN IF NOT EXISTS certificate_template_url text;")
    conn.commit()
    print("Added certificate_template_url column successfully.")
except Exception as e:
    print(f"Error: {e}")
    conn.rollback()
conn.close()
