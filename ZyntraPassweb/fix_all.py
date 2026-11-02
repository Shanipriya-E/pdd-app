with open('c:/Users/Vishnu/OneDrive/Desktop/ZyntraPassweb/participants.html', 'r', encoding='utf-8') as f:
    html = f.read()

parts = html.split('<script>', 1)
base_html = parts[0]
base_html = base_html.replace('<title>ZyntraPass - Participants</title>', '<title>ZyntraPass - Live Attendance</title>')
base_html = base_html.replace('<h1 class="title">Participants</h1>', '<h1 class="title">Live Attendance</h1>')
base_html = base_html.replace('<p class="subtitle">Review and manage join requests.</p>', '<p class="subtitle">Monitor real-time GPS check-ins for your ongoing events.</p>')

script = """<script>
    const SUPABASE_URL  = 'https://qokgtrabcxtxlympbkyb.supabase.co';
    const SUPABASE_ANON = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFva2d0cmFiY3h0eGx5bXBia3liIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODczODMyMDYsImV4cCI6MjEwMjk1OTIwNn0.hbs5MZ4FiqUoZxDTrGqtMPOjRbbKUupgZOcoeLZa3ME';
    let sb, currentUserId;
    
    const navItems = document.querySelectorAll('.sidebar-item, .nav-item');
    navItems.forEach(el => {
        if(el.textContent.includes('Live')) el.classList.add('active');
        else el.classList.remove('active');
    });
    document.querySelectorAll('.sidebar-item, .nav-item').forEach(el => {
        if(el.textContent.includes('Live')) el.href = 'live.html';
        if(el.textContent.includes('Participants')) el.href = 'participants.html';
        if(el.textContent.includes('Events')) el.href = 'events.html';
        if(el.textContent.includes('Dashboard')) el.href = 'dashboard.html';
    });

    async function main() {
        sb = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON);
        const { data: { session } } = await sb.auth.getSession();
        if (!session) { window.location.href = 'index.html'; return; }
        currentUserId = session.user.id;
        loadEvents();
    }

    function escHtml(str) {
        if (!str) return '';
        return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;');
    }
    
    function computeStatus(ev) {
        const now = new Date();
        const start = ev.start_date ? new Date(ev.start_date) : null;
        const end = ev.end_date ? new Date(ev.end_date) : null;
        if (!start || !end) return 'upcoming';
        if (now < start) return 'upcoming';
        if (now > end) return 'completed';
        return 'ongoing';
    }

    let allEvents = [];
    
    async function loadEvents() {
        const accessToken = (await sb.auth.getSession()).data.session.access_token;
        const container = document.getElementById('main-container');
        container.innerHTML = '<div style="text-align:center;padding:20px;color:#64748b;">Loading ongoing events...</div>';
        
        const res = await fetch(`${SUPABASE_URL}/rest/v1/events?organizer_id=eq.${currentUserId}&select=id,title,banner_image_url,start_date,end_date,checkpoints_count&order=created_at.desc`, {
            headers: { 'apikey': SUPABASE_ANON, 'Authorization': 'Bearer ' + accessToken }
        });
        const events = await res.json();
        
        allEvents = events.filter(e => {
            const st = computeStatus(e);
            return st === 'ongoing' || st === 'upcoming' || st === 'completed';
        });
        
        renderEventsList();
    }

    function renderEventsList() {
        const container = document.getElementById('main-container');
        if (allEvents.length === 0) {
            container.innerHTML = '<div style="text-align:center;padding:40px;color:#64748b;">No events to track.</div>';
            return;
        }

        let html = '';
        allEvents.forEach(ev => {
            const status = computeStatus(ev);
            const chipClass = `chip-${status}`;
            const thumb = ev.banner_image_url 
                ? `<img src="${escHtml(ev.banner_image_url)}" class="event-thumb" onerror="this.outerHTML='<div class=\\'event-thumb\\'>📍</div>'">`
                : `<div class="event-thumb">📍</div>`;

            html += `
            <div class="event-item" onclick="renderLiveDetail('${ev.id}')">
                ${thumb}
                <div class="event-item-body">
                    <div class="event-item-title">${escHtml(ev.title || 'Untitled')}</div>
                    <span class="event-status-chip ${chipClass}">${status}</span>
                </div>
                <div style="font-size:24px; color:#cbd5e1;">&rsaquo;</div>
            </div>`;
        });
        container.innerHTML = html;
    }

    let profileMap = {};
    let liveInterval = null;

    async function renderLiveDetail(eventId) {
        const container = document.getElementById('main-container');
        container.innerHTML = '<div style="text-align:center;padding:40px;">Fetching live GPS logs...</div>';
        
        const ev = allEvents.find(e => e.id === eventId);
        const accessToken = (await sb.auth.getSession()).data.session.access_token;
        
        const res = await fetch(`${SUPABASE_URL}/rest/v1/event_registrations?event_id=eq.${eventId}&status=eq.approved&select=id,attendee_id`, {
            headers: { 'apikey': SUPABASE_ANON, 'Authorization': 'Bearer ' + accessToken, 'cache': 'no-store' }
        });
        const regs = await res.json();
        
        if (!Array.isArray(regs) || regs.length === 0) {
            container.innerHTML = `
                <button class="back-btn" onclick="renderEventsList()">🔙 Back</button>
                <h1 class="page-title">${escHtml(ev.title)}</h1>
                <div style="text-align:center;padding:40px;color:#64748b;">No approved participants to track.</div>
            `;
            return;
        }

        const uids = regs.map(r => `"${r.attendee_id}"`).join(',');
        
        // Fetch profiles
        const pRes = await fetch(`${SUPABASE_URL}/rest/v1/profiles?id=in.(${uids})&select=id,full_name,email`, {
            headers: { 'apikey': SUPABASE_ANON, 'Authorization': 'Bearer ' + accessToken }
        });
        const profiles = await pRes.json();
        if (Array.isArray(profiles)) {
            profiles.forEach(p => profileMap[p.id] = p);
        }
        
        // Fetch attendee_profiles
        const apRes = await fetch(`${SUPABASE_URL}/rest/v1/attendee_profiles?id=in.(${uids})&select=*`, {
            headers: { 'apikey': SUPABASE_ANON, 'Authorization': 'Bearer ' + accessToken }
        });
        const aProfiles = await apRes.json();
        if (Array.isArray(aProfiles)) {
            aProfiles.forEach(p => {
                if (!profileMap[p.id] || !profileMap[p.id].full_name) {
                    profileMap[p.id] = { ...(profileMap[p.id] || {}), ...p };
                }
            });
        }

        fetchLiveStats(eventId, regs, ev);
        
        if (liveInterval) clearInterval(liveInterval);
        liveInterval = setInterval(() => {
            if (document.getElementById('main-container').innerHTML.includes('participant-grid')) {
                fetchLiveStats(eventId, regs, ev, true);
            } else {
                clearInterval(liveInterval);
            }
        }, 10000);
    }
    
    async function fetchLiveStats(eventId, regs, ev, isSilent = false) {
        const container = document.getElementById('main-container');
        const accessToken = (await sb.auth.getSession()).data.session.access_token;
        
        const logsRes = await fetch(`${SUPABASE_URL}/rest/v1/attendance_logs?event_id=eq.${eventId}&select=attendee_id,checkpoint_index`, {
            headers: { 'apikey': SUPABASE_ANON, 'Authorization': 'Bearer ' + accessToken, 'cache': 'no-store' }
        });
        const allLogs = await logsRes.json();
        
        const cpCounts = {};
        if (Array.isArray(allLogs)) {
            allLogs.forEach(lg => {
                cpCounts[lg.attendee_id] = (cpCounts[lg.attendee_id] || 0) + 1;
            });
        }
        
        const totalCp = ev.checkpoints_count || 4;
        
        const now = new Date();
        const start = ev.start_date ? new Date(ev.start_date) : null;
        const end = ev.end_date ? new Date(ev.end_date) : null;
        let elapsedSessions = 0;
        
        if (start && end) {
            if (now >= end) {
                elapsedSessions = totalCp;
            } else if (now >= start) {
                const durationMs = end.getTime() - start.getTime();
                const windowMs = durationMs / totalCp;
                const elapsedMs = now.getTime() - start.getTime();
                elapsedSessions = Math.floor(elapsedMs / windowMs);
            }
        }
        
        let html = `
            <button class="back-btn" onclick="renderEventsList(); if(liveInterval) clearInterval(liveInterval);" style="margin-bottom:16px;">🔙 Back to Events</button>
            <h1 class="page-title" style="margin-bottom:4px;">${escHtml(ev.title)}</h1>
            <p class="page-subtitle">Live GPS Attendance Tracking • Auto-updates every 10s</p>
            <div class="participant-grid" style="display:grid; gap:16px; margin-top:20px;">
        `;
        
        regs.forEach(r => {
            const p = profileMap[r.attendee_id] || {};
            const name = p.full_name || 'Unknown Participant';
            const initials = name.split(' ').map(n=>n[0]).join('').substring(0,2).toUpperCase();
            
            const attended = cpCounts[r.attendee_id] || 0;
            const missed = Math.max(0, elapsedSessions - attended);
            const remaining = Math.max(0, totalCp - elapsedSessions);
            
            const percent = Math.min(100, Math.round((attended / totalCp) * 100));
            const barColor = percent >= 80 ? '#10b981' : (percent >= 50 ? '#f59e0b' : '#ef4444');
            
            html += `
            <div class="event-item" style="display:flex; flex-direction:column; gap:12px; cursor:default; background:white; border-radius:16px; padding:16px; border:1px solid #e2e8f0; box-shadow:0 1px 3px rgba(0,0,0,0.05);">
                <div style="align-items: center; display: flex; gap: 16px;">
                    <div class="event-thumb" style="width:48px; height:48px; font-size:18px; border-radius:50%; background:#f1f5f9; color:#475569; display:flex; align-items:center; justify-content:center; font-weight:bold;">${initials}</div>
                    <div style="flex:1;">
                        <div class="event-item-title" style="font-size:16px; font-weight:700; color:#0f172a;">${escHtml(name)}</div>
                        <div style="display:flex; gap:12px; margin-top:4px;">
                            <span style="font-size:12px; font-weight:600; color:#10b981;">✅ ${attended} Attended</span>
                            <span style="font-size:12px; font-weight:600; color:#ef4444;">❌ ${missed} Missed</span>
                            <span style="font-size:12px; font-weight:600; color:#64748b;">⏳ ${remaining} Remaining</span>
                        </div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:24px; font-weight:800; color:${barColor};">${percent}%</div>
                        <div style="font-size:11px; color:#64748b; font-weight:600; text-transform:uppercase;">Attendance</div>
                    </div>
                </div>
                <div style="background:#f1f5f9; height:8px; border-radius:4px; overflow:hidden; width:100%;">
                    <div style="background:${barColor}; width:${percent}%; height:100%; transition:width 0.5s ease;"></div>
                </div>
            </div>`;
        });
        
        html += `</div>`;
        container.innerHTML = html;
    }

    document.addEventListener("DOMContentLoaded", main);
</script>
</body>
</html>
"""

with open('c:/Users/Vishnu/OneDrive/Desktop/ZyntraPassweb/live.html', 'w', encoding='utf-8') as f:
    f.write(base_html + script)

print("Rewrote live.html completely!")
