import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DB_PASSWORD = os.environ.get("SUPABASE_DB_PASSWORD")

try:
    conn = psycopg2.connect(
        host="aws-0-ap-south-1.pooler.supabase.com",
        database="postgres",
        user="postgres.qokgtrabcxtxlympbkyb",
        password=DB_PASSWORD,
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
        password=DB_PASSWORD,
        port="5432"
    )
    cur = conn2.cursor()
    cur.execute("SELECT policyname, cmd, qual, with_check FROM pg_policies WHERE tablename = 'event_registrations';")
    print("Policies 2:", cur.fetchall())
except Exception as e:
    print("Error 2:", e)
