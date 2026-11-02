import re

with open('c:/Users/Vishnu/OneDrive/Desktop/ZyntraPassweb/live.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_func = """    async function fetchLiveStats(eventId, regs, ev, isSilent = false) {
        const container = document.getElementById('main-container');
        const accessToken = (await sb.auth.getSession()).data.session.access_token;
        
        const logsRes = await fetch(`${SUPABASE_URL}/rest/v1/attendance_logs?event_id=eq.${eventId}&select=attendee_id,checkpoint_index`, {
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
        
        // Calculate elapsed sessions based on time
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
            // Missed is elapsed sessions minus attended (bounded to at least 0)
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
    }"""

content = re.sub(r'\s*async function fetchLiveStats.*?\}\s*(?=document\.addEventListener)', '\n\n' + new_func + '\n\n    ', content, flags=re.DOTALL)

with open('c:/Users/Vishnu/OneDrive/Desktop/ZyntraPassweb/live.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated fetchLiveStats logic!")
