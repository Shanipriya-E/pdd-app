import psycopg2
conn = psycopg2.connect('postgresql://postgres:Harsha%4020042006@db.qokgtrabcxtxlympbkyb.supabase.co:5432/postgres')
cur = conn.cursor()

cur.execute("""
CREATE OR REPLACE FUNCTION volunteer_get_event_stats(v_code TEXT, e_id UUID)
RETURNS json
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    is_valid BOOLEAN;
    res json;
BEGIN
    SELECT EXISTS (
        SELECT 1 FROM volunteers 
        WHERE secret_code = v_code AND event_id = e_id AND status = 'approved'
    ) INTO is_valid;

    IF NOT is_valid THEN
        RAISE EXCEPTION 'Invalid volunteer code or not approved for this event.';
    END IF;

    SELECT json_build_object(
        'total_registered', (SELECT count(*) FROM event_registrations WHERE event_id = e_id),
        'approved', (SELECT count(*) FROM event_registrations WHERE event_id = e_id AND status = 'approved'),
        'rejected', (SELECT count(*) FROM event_registrations WHERE event_id = e_id AND status = 'cancelled'),
        'attended', (SELECT count(*) FROM event_registrations WHERE event_id = e_id AND status = 'attended')
    ) INTO res;

    RETURN res;
END;
$$;
""")
conn.commit()
print("RPC updated successfully.")
conn.close()
