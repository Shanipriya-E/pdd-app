import psycopg2

password = "Harsha@20042006"
host = "db.qokgtrabcxtxlympbkyb.supabase.co"

print("Connecting to the database...")
try:
    conn = psycopg2.connect(
        host=host,
        database="postgres",
        user="postgres",
        password=password,
        port="5432"
    )
    conn.autocommit = True
    cur = conn.cursor()
    
    print("Executing SQL to update check constraint...")
    sql = """
    ALTER TABLE event_registrations 
    DROP CONSTRAINT IF EXISTS event_registrations_status_check;

    ALTER TABLE event_registrations 
    ADD CONSTRAINT event_registrations_status_check 
    CHECK (status IN ('registered', 'approved', 'rejected', 'attended', 'cancelled'));
    """
    cur.execute(sql)
    print("Successfully updated the check constraint!")
    
except Exception as e:
    print("Error:", e)
