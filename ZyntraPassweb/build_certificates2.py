import re

with open('events.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix active state in sidebar
html = html.replace('href="events.html" class="sidebar-item active"', 'href="events.html" class="sidebar-item"')
html = html.replace('href="#" class="sidebar-item"><span>??</span> Certificates', 'href="certificates.html" class="sidebar-item active"><span>??</span> Certificates')

# Replace container content
main_content = '''<div class="container" style="max-width: 800px;">
    <h1 style="font-size: 28px; font-weight: 800; color: #0f172a; margin-bottom: 8px;">Certificates</h1>
    <p class="subtitle">Manage and issue certificates for completed events.</p>

    <!-- Event List -->
    <div id="events-list" style="display: flex; flex-direction: column; gap: 16px; margin-top: 24px;">
        <p>Loading completed events...</p>
    </div>

    <!-- Event Details & Issue Modal -->
    <div class="modal-overlay" id="cert-modal">
        <div class="modal-content" style="max-width: 600px; padding: 24px; position:relative;">
            <button onclick="document.getElementById('cert-modal').classList.remove('active')" style="position:absolute; right:20px; top:20px; background:none; border:none; font-size:24px; cursor:pointer;">×</button>
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
'''

# We need to replace everything from <div class="container"> to the bottom nav.
html = re.sub(r'<div class="container">.*?<!-- ?? Bottom Nav ?? -->', main_content + '\n<!-- ?? Bottom Nav ?? -->', html, flags=re.DOTALL)

# Inject CSS for Modal if missing
css_inject = '''
        .modal-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); z-index: 1000; display: none; align-items: center; justify-content: center; }
        .modal-overlay.active { display: flex; }
        .modal-content { background: white; border-radius: 16px; width: 90%; max-width: 400px; position: relative; }
        
        .event-card { background: white; border: 1px solid #e2e8f0; border-radius: 16px; padding: 20px; cursor: pointer; transition: transform 0.2s, box-shadow 0.2s; }
        .event-card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.05); border-color: #cbd5e1; }
        .event-card h3 { font-size: 18px; color: #0f172a; margin-bottom: 8px; }
        .event-card p { font-size: 14px; color: #64748b; margin-bottom:0; }
'''
html = html.replace('</style>', css_inject + '\n    </style>')

# Replace the main() function logic
script_logic = '''
    let currentEventId = null;
    let eligibleAttendees = [];

    async function main() {
        sb = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON);
        const { data: { session } } = await sb.auth.getSession();
        if (!session) { window.location.href = 'index.html'; return; }
        
        currentUserId = session.user.id;
        currentUserEmail = session.user.email;
        
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

        loadCompletedEvents();
        
        document.getElementById('btn-upload-template').addEventListener('click', () => {
            document.getElementById('template-upload').click();
        });
        
        document.getElementById('template-upload').addEventListener('change', handleTemplateUpload);
        document.getElementById('btn-issue-certs').addEventListener('click', issueCertificates);
    }

    async function loadCompletedEvents() {
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
        
        // Filter events where end_date <= today
        const completed = events.filter(e => e.end_date && e.end_date <= now.split('T')[0]);
        
        if (completed.length === 0) {
            listDiv.innerHTML = '<p style="color:#64748b;">No completed events found. Certificates can only be issued after an event has ended.</p>';
            return;
        }
        
        listDiv.innerHTML = '';
        completed.forEach(ev => {
            const card = document.createElement('div');
            card.className = 'event-card';
            card.innerHTML = 
                <h3></h3>
                <p>Completed on </p>
                
            ;
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
        
        const fileName = certificate__.;
        
        const { data: uploadData, error: uploadError } = await sb.storage.from('certificates').upload(fileName, file, { cacheControl: '3600', upsert: true });
        
        if (uploadError) {
            alert("Upload failed: " + uploadError.message);
            btn.textContent = "Upload New Template (Image)";
            btn.disabled = false;
            return;
        }
        
        const { data: { publicUrl } } = sb.storage.from('certificates').getPublicUrl(fileName);
        
        // Save to events table
        const { error: updateError } = await sb.from('events').update({ certificate_template_url: publicUrl }).eq('id', currentEventId);
        if (updateError) {
            alert("Failed to save template URL.");
            btn.textContent = "Upload New Template (Image)";
            btn.disabled = false;
            return;
        }
        
        // Refresh
        const { data: ev } = await sb.from('events').select('*').eq('id', currentEventId).single();
        document.getElementById('btn-upload-template').disabled = false;
        loadCompletedEvents();
        openEventModal(ev);
    }

    async function loadEligibleAttendees(ev) {
        const section = document.getElementById('eligible-section');
        const listDiv = document.getElementById('eligible-list');
        const countP = document.getElementById('eligible-count');
        
        section.style.display = 'block';
        listDiv.innerHTML = "Calculating attendance...";
        
        // Fetch all registrations and attendance logs
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
        let html = '';
        
        for (const reg of regs) {
            const attendeeLogs = logs.filter(l => l.attendee_id === reg.attendee_id);
            const uniqueCheckpoints = new Set(attendeeLogs.map(l => l.checkpoint_index)).size;
            
            const attendancePercent = (uniqueCheckpoints / requiredCheckpoints) * 100;
            
            if (attendancePercent >= 80) {
                const name = reg.profiles ? reg.profiles.full_name : 'Unknown User';
                const isIssued = issuedSet.has(reg.attendee_id);
                if (!isIssued) eligibleAttendees.push(reg.attendee_id);
                
                html += <div style="padding: 4px 0; border-bottom: 1px solid #f1f5f9; display: flex; justify-content: space-between;">
                    <span></span>
                    <span style="color: ; font-size:12px; font-weight:bold;"> (%)</span>
                </div>;
            }
        }
        
        if (html === '') html = "No attendees met the 80% attendance requirement.";
        listDiv.innerHTML = html;
        countP.textContent = ${eligibleAttendees.length} unissued eligible participants found.;
        
        const issueBtn = document.getElementById('btn-issue-certs');
        if (eligibleAttendees.length > 0) {
            issueBtn.style.display = 'block';
            issueBtn.textContent = Issue Certificates ();
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
            status.textContent = Successfully issued  certificates!;
            status.style.color = '#16a34a';
            btn.style.display = 'none';
            // Refresh modal
            const { data: ev } = await sb.from('events').select('*').eq('id', currentEventId).single();
            loadEligibleAttendees(ev);
        }
    }
'''

html = re.sub(r'async function main\(\) \{.*', script_logic + '\nmain();\n</script>\n</body>\n</html>', html, flags=re.DOTALL)

with open('certificates.html', 'w', encoding='utf-8') as f:
    f.write(html)
