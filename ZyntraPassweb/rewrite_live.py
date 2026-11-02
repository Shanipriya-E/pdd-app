import re

with open('c:/Users/Vishnu/OneDrive/Desktop/ZyntraPassweb/live.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the whole <script> block at the bottom
new_script = """<script>
    const SUPABASE_URL  = 'https://qokgtrabcxtxlympbkyb.supabase.co';
    const SUPABASE_ANON = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFva2d0cmFiY3h0eGx5bXBia3liIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODczODMyMDYsImV4cCI6MjEwMjk1OTIwNn0.hbs5MZ4FiqUoZxDTrGqtMPOjRbbKUupgZOcoeLZa3ME';
    let sb, currentUserId;
    
    // UI mapping
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
        const container = document.getElementById('eventsList');
        container.innerHTML = '<div style="text-align:center;padding:20px;color:#64748b;">Loading ongoing events...</div>';
        
        const res = await fetch(`${SUPABASE_URL}/rest/v1/events?organizer_id=eq.${currentUserId}&select=id,title,banner_image_url,start_date,end_date,checkpoints_count&order=created_at.desc`, {
            headers: { 'apikey': SUPABASE_ANON, 'Authorization': 'Bearer ' + accessToken }
        });
        const events = await res.json();
        
        // Filter only ongoing or completed for live tracking
        allEvents = events.filter(e => {
            const st = computeStatus(e);
            return st === 'ongoing' || st === 'upcoming' || st === 'completed';
        });
        
        renderEventsList();
    }

    function renderEventsList() {
        const container = document.getElementById('eventsList');
        document.getElementById('eventDetail').style.display = 'none';
        container.style.display = 'block';
        document.getElementById('participantModal').classList.remove('active');
        
        if (allEvents.length === 0) {
            container.innerHTML = '<div style="text-align:center;padding:40px;color:#64748b;">No events to track.</div>';
            return;
        }

        let html = '';
        allEvents.forEach(ev => {
            const status = computeStatus(ev);
            const chipClass = `chip-${status}`;
            const thumb = ev.banner_image_url 
                ? `<img src="${escHtml(ev.banner_image_url)}" class="event-thumb" onerror="this.outerHTML='<div class=\\'event-thumb\\'>??</div>'">`
                : `<div class="event-thumb">📍</div>`;
            const safeTitle = (ev.title || '').replace(/'/g, "\\'").replace(/"/g, "&quot;");

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
        document.getElementById('eventsList').style.display = 'none';
        const container = document.getElementById('eventDetail');
        container.style.display = 'block';
        container.innerHTML = '<div style="text-align:center;padding:40px;">Fetching live GPS logs...</div>';
        
        const ev = allEvents.find(e => e.id === eventId);
        const accessToken = (await sb.auth.getSession()).data.session.access_token;
        
        // Fetch approved participants
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

        // Fetch profiles
        const uids = regs.map(r => `"${r.attendee_id}"`).join(',');
        const pRes = await fetch(`${SUPABASE_URL}/rest/v1/profiles?id=in.(${uids})&select=id,full_name,email`, {
            headers: { 'apikey': SUPABASE_ANON, 'Authorization': 'Bearer ' + accessToken }
        });
        const profiles = await pRes.json();
        if (Array.isArray(profiles)) {
            profiles.forEach(p => profileMap[p.id] = p);
        }

        fetchLiveStats(eventId, regs, ev);
        
        // Auto refresh every 10 seconds
        if (liveInterval) clearInterval(liveInterval);
        liveInterval = setInterval(() => {
            if (document.getElementById('eventsList').style.display === 'none') {
                fetchLiveStats(eventId, regs, ev, true);
            } else {
                clearInterval(liveInterval);
            }
        }, 10000);
    }
    
    async function fetchLiveStats(eventId, regs, ev, isSilent = false) {
        const container = document.getElementById('eventDetail');
        const accessToken = (await sb.auth.getSession()).data.session.access_token;
        
        const logsRes = await fetch(`${SUPABASE_URL}/rest/v1/attendance_logs?event_id=eq.${eventId}&select=attendee_id`, {
            headers: { 'apikey': SUPABASE_ANON, 'Authorization': 'Bearer ' + accessToken, 'cache': 'no-store' }
        });
        const allLogs = await logsRes.json();
        
        // Count checkpoints per attendee
        const cpCounts = {};
        if (Array.isArray(allLogs)) {
            allLogs.forEach(lg => {
                cpCounts[lg.attendee_id] = (cpCounts[lg.attendee_id] || 0) + 1;
            });
        }
        
        const totalCp = ev.checkpoints_count || 4;
        
        let html = `
            <button class="back-btn" onclick="renderEventsList(); if(liveInterval) clearInterval(liveInterval);">🔙 Back</button>
            <h1 class="page-title" style="margin-bottom:4px;">${escHtml(ev.title)}</h1>
            <p class="page-subtitle">Live GPS Attendance Tracking • Auto-updates every 10s</p>
            <div class="participant-grid">
        `;
        
        regs.forEach(r => {
            const p = profileMap[r.attendee_id] || {};
            const name = p.full_name || 'Unknown';
            const initials = name.split(' ').map(n=>n[0]).join('').substring(0,2).toUpperCase();
            
            const verified = cpCounts[r.attendee_id] || 0;
            const percent = Math.min(100, Math.round((verified / totalCp) * 100));
            
            html += `
            <div class="participant-card">
                <div class="p-card-top" style="align-items: center; display: flex; gap: 12px; margin-bottom: 12px;">
                    <div class="p-avatar" style="width:40px; height:40px; font-size:16px;">${initials}</div>
                    <div class="p-info" style="flex:1;">
                        <div class="p-name">${escHtml(name)}</div>
                        <div class="p-sub" style="font-size:12px; color:#64748b;">${verified} of ${totalCp} checkpoints</div>
                    </div>
                    <div style="font-size:20px; font-weight:700; color:${percent >= 80 ? '#10b981' : '#3b82f6'};">${percent}%</div>
                </div>
                <div style="background:#e2e8f0; height:8px; border-radius:4px; overflow:hidden;">
                    <div style="background:${percent >= 80 ? '#10b981' : '#3b82f6'}; width:${percent}%; height:100%; transition:width 0.3s;"></div>
                </div>
            </div>`;
        });
        
        html += `</div>`;
        
        if (!isSilent || !container.innerHTML.includes('participant-grid')) {
            container.innerHTML = html;
        } else {
            // Soft update if possible (re-rendering whole thing for simplicity since it's small)
            container.innerHTML = html;
        }
    }

    document.addEventListener("DOMContentLoaded", main);
</script>"""

# Replace script
content = re.sub(r'<script>.*?</script>', new_script, content, flags=re.DOTALL)

with open('c:/Users/Vishnu/OneDrive/Desktop/ZyntraPassweb/live.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated live.html logic")
