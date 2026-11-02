# -*- coding: utf-8 -*-
with open('certificates.html', 'w', encoding='utf-8') as f:
    f.write(r'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZyntraPass - Certificates</title>
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
        body { background-color: #f7f9fc; color: #0d162a; padding-bottom: 70px; }
        
        .top-bar { background-color: white; padding: 16px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #e2e8f0; position: sticky; top: 0; z-index: 100; }
        .btn-menu { background: white; border: 1px solid #e2e8f0; border-radius: 12px; width: 44px; height: 44px; font-size: 20px; cursor: pointer; color: #0d162a; }
        .header-actions { display: flex; gap: 12px; align-items: center; }
        
        .container { padding: 24px; max-width: 800px; margin: 0 auto; }
        .page-title { font-size: 28px; font-weight: 800; color: #0f172a; margin-bottom: 8px; }
        .subtitle { font-size: 15px; color: #475569; line-height: 1.5; margin-bottom: 24px; }
        
        .btn-create { background-color: #5b54e3; color: white; border: none; border-radius: 12px; padding: 14px 24px; font-weight: 600; font-size: 15px; cursor: pointer; display: inline-flex; align-items: center; justify-content: center; gap: 8px; }
        .btn-create:hover { background-color: #4a44b8; }
        .btn-create:disabled { background-color: #94a3b8; cursor: not-allowed; }

        .modal-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); z-index: 1000; display: none; align-items: center; justify-content: center; }
        .modal-overlay.active { display: flex; }
        .modal-content { background: white; border-radius: 16px; width: 90%; max-width: 600px; padding: 24px; position: relative; max-height: 90vh; overflow-y: auto; }
        
        .event-card { background: white; border: 1px solid #e2e8f0; border-radius: 16px; padding: 20px; cursor: pointer; transition: transform 0.2s, box-shadow 0.2s; }
        .event-card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.05); border-color: #cbd5e1; }
        .event-card h3 { font-size: 18px; color: #0f172a; margin-bottom: 8px; }
        .event-card p { font-size: 14px; color: #64748b; margin-bottom:0; }

        /* Sidebar Drawer */
        .sidebar-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); z-index: 999; display: none; }
        .sidebar-overlay.active { display: block; }
        .sidebar { position: fixed; top: 0; left: -300px; bottom: 0; width: 300px; background: linear-gradient(180deg, #1A448C 0%, #0D162A 100%); z-index: 1000; transition: left 0.3s ease; display: flex; flex-direction: column; color: white; box-shadow: 4px 0 16px rgba(0,0,0,0.2); }
        .sidebar.active { left: 0; }
        .sidebar-header { padding: 24px; display: flex; align-items: center; gap: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); }
        .sidebar-logo-icon { width: 40px; height: 40px; background-color: #5B54E3; border-radius: 12px; display: flex; justify-content: center; align-items: center; font-size: 20px; }
        .sidebar-brand { font-size: 18px; font-weight: bold; margin: 0; }
        .sidebar-subbrand { font-size: 12px; color: #A8B2D1; margin: 0; }
        .sidebar-menu { flex: 1; overflow-y: auto; padding: 16px 0; display: flex; flex-direction: column; gap: 4px; }
        .sidebar-item { padding: 12px 24px; display: flex; align-items: center; gap: 16px; color: #E2E8F0; text-decoration: none; font-weight: 600; font-size: 14px; }
        .sidebar-item:hover, .sidebar-item.active { background-color: rgba(255,255,255,0.1); color: white; }
        .sidebar-footer { padding: 24px; border-top: 1px solid rgba(255,255,255,0.1); display: flex; align-items: center; gap: 12px; }
        .sidebar-footer .avatar { width: 40px; height: 40px; background-color: #3C4260; color: #A8B2D1; font-size: 14px; display: flex; align-items: center; justify-content: center; font-weight: bold; border-radius: 50%; }
        .sidebar-user-info { flex: 1; }
        .sidebar-user-name { margin: 0; font-weight: bold; font-size: 14px; color: white; }
        .sidebar-user-email { margin: 0; font-size: 11px; color: #A8B2D1; }
        .sidebar-logout { font-size: 20px; color: #A8B2D1; cursor: pointer; }
        .sidebar-logout:hover { color: white; }
    </style>
</head>
<body>

    <!-- Sidebar -->
    <div class="sidebar-overlay" id="sidebar-overlay"></div>
    <div class="sidebar" id="sidebar">
        <div class="sidebar-header">
            <div class="sidebar-logo-icon">✨</div>
            <div>
                <p class="sidebar-brand">ZyntraPass</p>
                <p class="sidebar-subbrand">Organizer workspace</p>
            </div>
        </div>
        <div class="sidebar-menu">
            <a href="dashboard.html" class="sidebar-item"><span>🏠</span> Dashboard</a>
            <a href="events.html" class="sidebar-item"><span>📅</span> Events</a>
            <a href="participants.html" class="sidebar-item"><span>👥</span> Participants</a>
            <a href="live.html" class="sidebar-item"><span>📡</span> Live Attendance</a>
            <a href="volunteers.html" class="sidebar-item"><span>🤝</span> Volunteers</a>
            <a href="certificates.html" class="sidebar-item active"><span>📜</span> Certificates</a>
            <a href="settings.html" class="sidebar-item"><span>⚙️</span> Settings</a>
        </div>
        <div class="sidebar-footer">
            <div class="avatar" id="sidebar-avatar">--</div>
            <div class="sidebar-user-info">
                <p class="sidebar-user-name" id="sidebar-name">Loading...</p>
                <p class="sidebar-user-email" id="sidebar-email">...</p>
            </div>
            <div class="sidebar-logout" id="sidebar-logout">🚪</div>
        </div>
    </div>

    <!-- Top App Bar -->
    <div class="top-bar">
        <button class="btn-menu" id="menuBtn">☰</button>
    </div>

    <!-- Main Content -->
    <div class="container">
        <h1 class="page-title">Certificates</h1>
        <p class="subtitle">Manage and issue certificates for completed events.</p>

        <div id="events-list" style="display: flex; flex-direction: column; gap: 16px; margin-top: 24px;">
            <p>Loading completed events...</p>
        </div>

        <div class="modal-overlay" id="cert-modal">
            <div class="modal-content">
                <button onclick="document.getElementById('cert-modal').classList.remove('active')" style="position:absolute; right:20px; top:20px; background:none; border:none; font-size:24px; cursor:pointer;">&#215;</button>
                <h2 id="modal-event-title" style="margin-bottom: 8px;">Event Title</h2>
                <p id="modal-event-date" style="color: #64748b; margin-bottom: 24px; font-size: 14px;">Date</p>
                
                <div id="template-section" style="background: #f8fafc; padding: 16px; border-radius: 12px; margin-bottom: 24px;">
                    <h3 style="font-size: 16px; margin-bottom: 12px;">Certificate Template</h3>
                    <img id="template-preview" src="" style="width: 100%; max-height: 200px; object-fit: contain; display: none; margin-bottom: 12px; border: 1px solid #e2e8f0; border-radius: 8px;" />
                    <input type="file" id="template-upload" accept="image/png, image/jpeg" style="display: none;" />
                    <button id="btn-upload-template" class="btn-create" style="width: 100%; padding:10px;">Upload New Template (Image)</button>
                    <p style="font-size: 12px; color: #64748b; margin-top: 8px;">Upload a blank certificate design. Attendees' names will be centered automatically.</p>
                </div>

                <div id="eligible-section" style="display: none;">
                    <h3 style="font-size: 16px; margin-bottom: 8px;">Eligible Participants (>80% Attendance)</h3>
                    <p id="eligible-count" style="font-size: 14px; color: #16a34a; margin-bottom: 12px;">0 participants qualify.</p>
                    
                    <div id="eligible-list" style="max-height: 200px; overflow-y: auto; background: #fff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px; margin-bottom: 24px; font-size: 14px;">
                    </div>

                    <button id="btn-issue-certs" class="btn-create" style="width: 100%; padding:10px;">Issue Certificates</button>
                    <div id="issue-status" style="margin-top: 8px; text-align: center; font-size: 14px; font-weight:bold;"></div>
                </div>
            </div>
        </div>
    </div>

<script>
    const SUPABASE_URL = 'https://qokgtrabcxtxlympbkyb.supabase.co';
    const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFva2d0cmFiY3h0eGx5bXBia3liIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODczODMyMDYsImV4cCI6MjEwMjk1OTIwNn0.hbs5MZ4FiqUoZxDTrGqtMPOjRbbKUupgZOcoeLZa3ME';

    let currentEventId = null;
    let eligibleAttendees = [];
    let sb;

    async function main() {
        sb = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
        const { data: { session } } = await sb.auth.getSession();
        if (!session) { window.location.href = 'index.html'; return; }
        
        let currentUserId = session.user.id;
        let currentUserEmail = session.user.email;
        
        // Sidebar wiring
        document.getElementById('sidebar-email').textContent = currentUserEmail;
        const sidebar = document.getElementById('sidebar');
        const overlay = document.getElementById('sidebar-overlay');
        document.getElementById('menuBtn').addEventListener('click', () => { sidebar.classList.add('active'); overlay.classList.add('active'); });
        overlay.addEventListener('click', () => { sidebar.classList.remove('active'); overlay.classList.remove('active'); });
        
        const logoutHandler = async () => { await sb.auth.signOut(); window.location.href = 'index.html'; };
        document.getElementById('sidebar-logout').addEventListener('click', logoutHandler);
        
        const { data: profile } = await sb.from('profiles').select('*').eq('id', currentUserId).maybeSingle();
        if (profile && profile.full_name) {
            const initials = profile.full_name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
            document.getElementById('sidebar-avatar').textContent = initials;
            document.getElementById('sidebar-name').textContent   = profile.full_name;
        }

        loadCompletedEvents(currentUserId);
        
        document.getElementById('btn-upload-template').addEventListener('click', () => {
            document.getElementById('template-upload').click();
        });
        
        document.getElementById('template-upload').addEventListener('change', handleTemplateUpload);
        document.getElementById('btn-issue-certs').addEventListener('click', issueCertificates);
    }

    async function loadCompletedEvents(currentUserId) {
        const listDiv = document.getElementById('events-list');
        listDiv.innerHTML = '<p>Loading...</p>';
        
        const now = new Date().toISOString();
        const { data: events, error } = await sb.from('events')
            .select('*')
            .eq('organizer_id', currentUserId)
            .order('end_date', { ascending: false });
            
        if (error) {
            console.error(error);
            listDiv.innerHTML = '<p style="color:red">Failed to load events.</p>';
            return;
        }
        
        const completed = events.filter(e => e.end_date && e.end_date <= now.split('T')[0]);
        
        if (completed.length === 0) {
            listDiv.innerHTML = '<p style="color:#64748b;">No completed events found. Certificates can only be issued after an event has ended.</p>';
            return;
        }
        
        listDiv.innerHTML = '';
        completed.forEach(ev => {
            const card = document.createElement('div');
            card.className = 'event-card';
            card.innerHTML = `
                <h3>${ev.title}</h3>
                <p>Completed on ${ev.end_date}</p>
                ${ev.certificate_template_url ? '<span style="display:inline-block; margin-top:8px; background:#dcfce7; color:#166534; padding:2px 8px; border-radius:12px; font-size:12px; font-weight:600;">Template Uploaded</span>' : '<span style="display:inline-block; margin-top:8px; background:#fee2e2; color:#991b1b; padding:2px 8px; border-radius:12px; font-size:12px; font-weight:600;">Action Required</span>'}
            `;
            card.onclick = () => openEventModal(ev);
            listDiv.appendChild(card);
        });
    }

    async function openEventModal(ev) {
        currentEventId = ev.id;
        document.getElementById('modal-event-title').textContent = ev.title;
        document.getElementById('modal-event-date').textContent = "Ended: " + ev.end_date;
        
        const preview = document.getElementById('template-preview');
        if (ev.certificate_template_url) {
            preview.src = ev.certificate_template_url;
            preview.style.display = 'block';
            document.getElementById('btn-upload-template').textContent = "Change Template";
            loadEligibleAttendees(ev);
        } else {
            preview.style.display = 'none';
            document.getElementById('btn-upload-template').textContent = "Upload Template";
            document.getElementById('eligible-section').style.display = 'none';
        }
        
        document.getElementById('issue-status').textContent = '';
        document.getElementById('cert-modal').classList.add('active');
    }

    async function handleTemplateUpload(e) {
        const file = e.target.files[0];
        if (!file) return;
        
        const btn = document.getElementById('btn-upload-template');
        btn.textContent = "Uploading...";
        btn.disabled = true;
        
        const fileName = `certificate_${currentEventId}_${Date.now()}.${file.name.split('.').pop()}`;
        
        const { data: uploadData, error: uploadError } = await sb.storage.from('certificates').upload(fileName, file, { cacheControl: '3600', upsert: true });
        
        if (uploadError) {
            alert("Upload failed: " + uploadError.message);
            btn.textContent = "Upload New Template (Image)";
            btn.disabled = false;
            return;
        }
        
        const { data: { publicUrl } } = sb.storage.from('certificates').getPublicUrl(fileName);
        
        const { error: updateError } = await sb.from('events').update({ certificate_template_url: publicUrl }).eq('id', currentEventId);
        if (updateError) {
            alert("Failed to save template URL.");
            btn.textContent = "Upload New Template (Image)";
            btn.disabled = false;
            return;
        }
        
        const { data: ev } = await sb.from('events').select('*').eq('id', currentEventId).single();
        document.getElementById('btn-upload-template').disabled = false;
        loadCompletedEvents(ev.organizer_id);
        openEventModal(ev);
    }

    async function loadEligibleAttendees(ev) {
        const section = document.getElementById('eligible-section');
        const listDiv = document.getElementById('eligible-list');
        const countP = document.getElementById('eligible-count');
        
        section.style.display = 'block';
        listDiv.innerHTML = "Calculating attendance...";
        
        const { data: regs } = await sb.from('event_registrations').select('attendee_id, profiles(full_name)').eq('event_id', currentEventId);
        const { data: logs } = await sb.from('attendance_logs').select('attendee_id, checkpoint_index').eq('event_id', currentEventId);
        const { data: certs } = await sb.from('certificates').select('attendee_id').eq('event_id', currentEventId);
        
        if (!regs || regs.length === 0) {
            listDiv.innerHTML = "No attendees registered.";
            countP.textContent = "0 participants qualify.";
            document.getElementById('btn-issue-certs').style.display = 'none';
            return;
        }
        
        const issuedSet = new Set(certs ? certs.map(c => c.attendee_id) : []);
        const requiredCheckpoints = ev.checkpoints_count || 1;
        
        eligibleAttendees = [];
        let htmlContent = '';
        
        for (const reg of regs) {
            const attendeeLogs = logs.filter(l => l.attendee_id === reg.attendee_id);
            const uniqueCheckpoints = new Set(attendeeLogs.map(l => l.checkpoint_index)).size;
            
            const attendancePercent = (uniqueCheckpoints / requiredCheckpoints) * 100;
            
            if (attendancePercent >= 80) {
                const name = reg.profiles ? reg.profiles.full_name : 'Unknown User';
                const isIssued = issuedSet.has(reg.attendee_id);
                if (!isIssued) eligibleAttendees.push(reg.attendee_id);
                
                htmlContent += `<div style="padding: 4px 0; border-bottom: 1px solid #f1f5f9; display: flex; justify-content: space-between;">
                    <span>${name}</span>
                    <span style="color: ${isIssued ? '#16a34a' : '#64748b'}; font-size:12px; font-weight:bold;">${isIssued ? 'Issued' : 'Eligible'} (${attendancePercent.toFixed(0)}%)</span>
                </div>`;
            }
        }
        
        if (htmlContent === '') htmlContent = "No attendees met the 80% attendance requirement.";
        listDiv.innerHTML = htmlContent;
        countP.textContent = `${eligibleAttendees.length} unissued eligible participants found.`;
        
        const issueBtn = document.getElementById('btn-issue-certs');
        if (eligibleAttendees.length > 0) {
            issueBtn.style.display = 'block';
            issueBtn.textContent = `Issue Certificates (${eligibleAttendees.length})`;
            issueBtn.disabled = false;
        } else {
            issueBtn.style.display = 'none';
        }
    }

    async function issueCertificates() {
        const btn = document.getElementById('btn-issue-certs');
        const status = document.getElementById('issue-status');
        
        btn.disabled = true;
        btn.textContent = "Issuing...";
        
        const inserts = eligibleAttendees.map(a_id => ({
            event_id: currentEventId,
            attendee_id: a_id
        }));
        
        const { error } = await sb.from('certificates').insert(inserts);
        
        if (error) {
            status.textContent = "Error issuing certificates: " + error.message;
            status.style.color = 'red';
            btn.disabled = false;
            btn.textContent = "Try Again";
        } else {
            status.textContent = `Successfully issued ${eligibleAttendees.length} certificates!`;
            status.style.color = '#16a34a';
            btn.style.display = 'none';
            const { data: ev } = await sb.from('events').select('*').eq('id', currentEventId).single();
            loadEligibleAttendees(ev);
        }
    }

    main();
</script>
</body>
</html>'''
    )
