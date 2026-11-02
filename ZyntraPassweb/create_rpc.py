import psycopg2
conn = psycopg2.connect('postgresql://postgres:Harsha%4020042006@db.qokgtrabcxtxlympbkyb.supabase.co:5432/postgres')
cur = conn.cursor()

cur.execute("""
CREATE OR REPLACE FUNCTION volunteer_scan_qr(v_code TEXT, e_id UUID, a_id UUID)
RETURNS BOOLEAN
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    is_valid BOOLEAN;
BEGIN
    -- Check if volunteer code is valid for this event
    SELECT EXISTS (
        SELECT 1 FROM volunteers 
        WHERE secret_code = v_code AND event_id = e_id AND status = 'approved'
    ) INTO is_valid;

    IF NOT is_valid THEN
        RAISE EXCEPTION 'Invalid volunteer code or not approved for this event.';
    END IF;

    -- Update attendee status
    UPDATE event_registrations 
    SET status = 'attended'
    WHERE event_id = e_id AND attendee_id = a_id;

    RETURN TRUE;
END;
$$;
""")
conn.commit()
print("RPC created successfully.")
conn.close()
