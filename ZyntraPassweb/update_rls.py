import psycopg2
conn = psycopg2.connect('postgresql://postgres:Harsha%4020042006@db.qokgtrabcxtxlympbkyb.supabase.co:5432/postgres')
cur = conn.cursor()

cur.execute("""
DROP POLICY IF EXISTS "Organizers can manage volunteers for their events" ON volunteers;

CREATE POLICY "Organizers can manage volunteers for their events"
ON volunteers FOR ALL
USING (
    event_id IN (
        SELECT id FROM events WHERE organizer_id = auth.uid()
    )
)
WITH CHECK (
    event_id IN (
        SELECT id FROM events WHERE organizer_id = auth.uid()
    )
);
""")
conn.commit()
print("Policy updated.")
conn.close()
