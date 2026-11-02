import psycopg2
conn = psycopg2.connect('postgresql://postgres:Harsha%4020042006@db.qokgtrabcxtxlympbkyb.supabase.co:5432/postgres')
cur = conn.cursor()

# Create table
cur.execute("""
CREATE TABLE IF NOT EXISTS volunteers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_id UUID REFERENCES events(id) ON DELETE CASCADE,
    user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
    status TEXT CHECK (status IN ('pending', 'approved', 'rejected')) DEFAULT 'pending',
    secret_code TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(event_id, user_id)
);

-- Enable RLS
ALTER TABLE volunteers ENABLE ROW LEVEL SECURITY;

-- Policy for attendees: can read own requests, can insert own requests
CREATE POLICY "Attendees can manage own volunteer requests"
ON volunteers FOR ALL
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

-- Policy for organizers: can read and update requests for their events
CREATE POLICY "Organizers can manage volunteers for their events"
ON volunteers FOR ALL
USING (
    EXISTS (
        SELECT 1 FROM events
        WHERE events.id = volunteers.event_id
        AND events.organizer_id = auth.uid()
    )
)
WITH CHECK (
    EXISTS (
        SELECT 1 FROM events
        WHERE events.id = volunteers.event_id
        AND events.organizer_id = auth.uid()
    )
);
""")
conn.commit()
print("Table created.")
conn.close()
