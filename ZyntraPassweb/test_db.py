import psycopg2

try:
    conn = psycopg2.connect(
        host="aws-0-ap-south-1.pooler.supabase.com", # often db host is different or needs pooler
        database="postgres",
        user="postgres.qokgtrabcxtxlympbkyb",
        password="YOUR_SUPABASE_DB_PASSWORD",  # Use env variable: os.environ['SUPABASE_DB_PASSWORD']
        port="5432"
    )
    cur = conn.cursor()
    cur.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public';")
    rows = cur.fetchall()
    print("Connected! Tables:", [r[0] for r in rows])
    
    cur.execute("SELECT policyname, cmd, qual, with_check FROM pg_policies WHERE tablename = 'event_registrations';")
    print("Policies:", cur.fetchall())
except Exception as e:
    print("Error 1:", e)

try:
    conn2 = psycopg2.connect(
        host="db.qokgtrabcxtxlympbkyb.supabase.co",
        database="postgres",
        user="postgres",
        password="YOUR_SUPABASE_DB_PASSWORD",  # Use env variable: os.environ['SUPABASE_DB_PASSWORD']
        port="5432"
    )
    cur = conn2.cursor()
    cur.execute("SELECT policyname, cmd, qual, with_check FROM pg_policies WHERE tablename = 'event_registrations';")
    print("Policies 2:", cur.fetchall())
except Exception as e:
    print("Error 2:", e)
