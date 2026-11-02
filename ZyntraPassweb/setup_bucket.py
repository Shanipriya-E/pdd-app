import psycopg2
conn = psycopg2.connect('postgresql://postgres:Harsha%4020042006@db.qokgtrabcxtxlympbkyb.supabase.co:5432/postgres')
cur = conn.cursor()
try:
    cur.execute("INSERT INTO storage.buckets (id, name, public) VALUES ('certificates', 'certificates', true) ON CONFLICT DO NOTHING;")
    cur.execute('CREATE POLICY "Certificates are publicly accessible." ON storage.objects FOR SELECT USING (bucket_id = \'certificates\');')
    cur.execute('CREATE POLICY "Organizers can upload certificates." ON storage.objects FOR INSERT WITH CHECK (bucket_id = \'certificates\' AND auth.role() = \'authenticated\');')
    cur.execute('CREATE POLICY "Organizers can update certificates." ON storage.objects FOR UPDATE USING (bucket_id = \'certificates\' AND auth.role() = \'authenticated\');')
    conn.commit()
    print("Bucket and policies created successfully.")
except Exception as e:
    print(f"Error: {e}")
    conn.rollback()
conn.close()
