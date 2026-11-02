-- ============================================================
-- ZyntraPass Database Schema & SQL Scripts
-- Generated: 2026-09-07
-- Database: Supabase (PostgreSQL)
-- ============================================================

-- ────────────────────────────────────────────────────────────
-- TABLE: event_registrations - status constraint update
-- ────────────────────────────────────────────────────────────
ALTER TABLE event_registrations
  DROP CONSTRAINT IF EXISTS event_registrations_status_check;

ALTER TABLE event_registrations
  ADD CONSTRAINT event_registrations_status_check
  CHECK (status IN ('registered', 'approved', 'rejected', 'attended', 'cancelled'));

-- ────────────────────────────────────────────────────────────
-- TABLE: attendance_logs
-- ────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS attendance_logs (
    id                UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    event_id          UUID            REFERENCES events(id) ON DELETE CASCADE,
    attendee_id       UUID            REFERENCES profiles(id) ON DELETE CASCADE,
    checkpoint_index  INTEGER         NOT NULL,
    latitude          DOUBLE PRECISION,
    longitude         DOUBLE PRECISION,
    timestamp         TIMESTAMPTZ     DEFAULT NOW(),
    UNIQUE(event_id, attendee_id, checkpoint_index)
);

ALTER TABLE attendance_logs ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Attendees can insert their own attendance" ON attendance_logs;
CREATE POLICY "Attendees can insert their own attendance"
ON attendance_logs FOR INSERT
WITH CHECK (auth.uid() = attendee_id);

DROP POLICY IF EXISTS "Attendees can read their own attendance" ON attendance_logs;
CREATE POLICY "Attendees can read their own attendance"
ON attendance_logs FOR SELECT
USING (auth.uid() = attendee_id);

DROP POLICY IF EXISTS "Organizers can read attendance for their events" ON attendance_logs;
CREATE POLICY "Organizers can read attendance for their events"
ON attendance_logs FOR SELECT
USING (
  event_id IN (
    SELECT id FROM events WHERE organizer_id = auth.uid()
  )
);

-- ────────────────────────────────────────────────────────────
-- TABLE: volunteers
-- ────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS volunteers (
    id          UUID    PRIMARY KEY DEFAULT gen_random_uuid(),
    event_id    UUID    REFERENCES events(id) ON DELETE CASCADE,
    user_id     UUID    REFERENCES profiles(id) ON DELETE CASCADE,
    status      TEXT    CHECK (status IN ('pending', 'approved', 'rejected')) DEFAULT 'pending',
    secret_code TEXT,
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(event_id, user_id)
);

ALTER TABLE volunteers ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Attendees can manage own volunteer requests"
ON volunteers FOR ALL
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

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

-- ────────────────────────────────────────────────────────────
-- FUNCTION: volunteer_scan_qr
-- Validates volunteer QR code and marks attendee as attended
-- ────────────────────────────────────────────────────────────
CREATE OR REPLACE FUNCTION volunteer_scan_qr(v_code TEXT, e_id UUID, a_id UUID)
RETURNS BOOLEAN
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    is_valid BOOLEAN;
BEGIN
    SELECT EXISTS (
        SELECT 1 FROM volunteers
        WHERE secret_code = v_code AND event_id = e_id AND status = 'approved'
    ) INTO is_valid;

    IF NOT is_valid THEN
        RAISE EXCEPTION 'Invalid volunteer code or not approved for this event.';
    END IF;

    UPDATE event_registrations
    SET status = 'attended'
    WHERE event_id = e_id AND attendee_id = a_id;

    RETURN TRUE;
END;
$$;

-- ────────────────────────────────────────────────────────────
-- FUNCTION: volunteer_get_event_stats
-- Returns event registration statistics for a volunteer
-- ────────────────────────────────────────────────────────────
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
        'approved',         (SELECT count(*) FROM event_registrations WHERE event_id = e_id AND status = 'approved'),
        'rejected',         (SELECT count(*) FROM event_registrations WHERE event_id = e_id AND status = 'cancelled'),
        'attended',         (SELECT count(*) FROM event_registrations WHERE event_id = e_id AND status = 'attended')
    ) INTO res;

    RETURN res;
END;
$$;

-- ============================================================
-- END OF SCHEMA SCRIPT
-- ============================================================
