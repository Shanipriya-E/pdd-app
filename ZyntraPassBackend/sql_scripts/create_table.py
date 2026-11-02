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
    
    print("Executing SQL to create attendance_logs...")
    sql = """
    CREATE TABLE IF NOT EXISTS attendance_logs (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        event_id UUID REFERENCES events(id) ON DELETE CASCADE,
        attendee_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
        checkpoint_index INTEGER NOT NULL,
        latitude DOUBLE PRECISION,
        longitude DOUBLE PRECISION,
        timestamp TIMESTAMPTZ DEFAULT NOW(),
        UNIQUE(event_id, attendee_id, checkpoint_index)
    );
    
    -- Enable RLS
    ALTER TABLE attendance_logs ENABLE ROW LEVEL SECURITY;
    
    -- Attendees can insert their own logs
    DROP POLICY IF EXISTS "Attendees can insert their own attendance" ON attendance_logs;
    CREATE POLICY "Attendees can insert their own attendance" 
    ON attendance_logs FOR INSERT 
    WITH CHECK (auth.uid() = attendee_id);
    
    -- Attendees can read their own logs
    DROP POLICY IF EXISTS "Attendees can read their own attendance" ON attendance_logs;
    CREATE POLICY "Attendees can read their own attendance" 
    ON attendance_logs FOR SELECT 
    USING (auth.uid() = attendee_id);
    
    -- Organizers can read logs for their events
    DROP POLICY IF EXISTS "Organizers can read attendance for their events" ON attendance_logs;
    CREATE POLICY "Organizers can read attendance for their events" 
    ON attendance_logs FOR SELECT 
    USING (
      event_id IN (
        SELECT id FROM events WHERE organizer_id = auth.uid()
      )
    );
    """
    cur.execute(sql)
    print("Successfully created attendance_logs and RLS policies!")
    
except Exception as e:
    print("Error:", e)
