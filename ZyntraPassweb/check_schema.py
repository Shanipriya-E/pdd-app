import psycopg2
conn = psycopg2.connect('postgresql://postgres:Harsha%4020042006@db.qokgtrabcxtxlympbkyb.supabase.co:5432/postgres')
cur = conn.cursor()

def print_schema(table):
    cur.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table}'")
    print(f"--- {table} ---")
    for row in cur.fetchall(): print(f"{row[0]}: {row[1]}")

print_schema('events')
print_schema('event_registrations')
print_schema('certificates')
conn.close()
