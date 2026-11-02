import psycopg2

password = "Harsha@20042006"
host = "db.qokgtrabcxtxlympbkyb.supabase.co"

conn = psycopg2.connect(host=host, database="postgres", user="postgres", password=password, port="5432")
conn.autocommit = True
cur = conn.cursor()

# Check current policies on attendance_logs
cur.execute("SELECT policyname, cmd FROM pg_policies WHERE tablename = 'attendance_logs';")
print("Current attendance_logs policies:")
for row in cur.fetchall():
    print(row)

# Make sure attendees can read their own logs
cur.execute("""
DROP POLICY IF EXISTS "Attendees can read their own attendance" ON attendance_logs;
CREATE POLICY "Attendees can read their own attendance"
ON attendance_logs FOR SELECT
USING (auth.uid() = attendee_id);
""")
print("RLS policy ensured for attendees to read their own attendance_logs.")

# Also mark registrations as 'attended' when they have at least 1 GPS log
# This keeps event_registrations in sync
cur.execute("""
UPDATE event_registrations er
SET status = 'attended'
WHERE status = 'approved'
AND EXISTS (
    SELECT 1 FROM attendance_logs al
    WHERE al.event_id = er.event_id
    AND al.attendee_id = er.attendee_id
);
""")
print(f"Updated {cur.rowcount} registration(s) to 'attended' based on GPS logs.")
