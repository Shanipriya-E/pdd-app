import re

with open('attendee_attendance.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_script = """<script>
    const SUPABASE_URL  = 'https://qokgtrabcxtxlympbkyb.supabase.co';
    const SUPABASE_ANON = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFva2d0cmFiY3h0eGx5bXBia3liIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODczODMyMDYsImV4cCI6MjEwMjk1OTIwNn0.hbs5MZ4FiqUoZxDTrGqtMPOjRbbKUupgZOcoeLZa3ME';

    let sb, currentUserId, currentUserEmail;
    let myEvents = [];
    let currentEventForLocation = null;
    let qrInterval, qrTimerInterval;
    let qrcodeObj = null;
    let locationWatchId = null;
    
    // Background tracking
    let globalLocationWatchId = null;
    let lastKnownLat = null, lastKnownLng = null;
    let locationActive = false;

    async function main() {
        sb = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON);
        const { data: { session } } = await sb.auth.getSession();
        if (!session) { window.location.href = 'index.html'; return; }

        currentUserId = session.user.id;
        currentUserEmail = session.user.email;
        document.getElementById('sidebar-email').textContent = currentUserEmail;

        const sidebar = document.getElementById('sidebar');
        const overlay = document.getElementById('sidebar-overlay');
        document.getElementById('menuBtn').addEventListener('click', () => { sidebar.classList.add('active'); overlay.classList.add('active'); });
        overlay.addEventListener('click', () => { sidebar.classList.remove('active'); overlay.classList.remove('active'); });
        document.getElementById('sidebar-logout').addEventListener('click', async () => {
            await sb.auth.signOut();
            window.location.href = 'index.html';
        });

        await loadAvatar();
        await loadAttendanceEvents();
        
        startBackgroundTracker();
        setInterval(evaluateCheckpoints, 10000); // Check every 10 seconds
    }

    async function loadAvatar() {
        const { data: profile } = await sb.from('profiles').select('full_name').eq('id', currentUserId).maybeSingle();
        if (profile && profile.full_name) {
            const initials = profile.full_name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
            document.getElementById('userAvatar').textContent = initials;
            document.getElementById('sidebar-avatar').textContent = initials;
            document.getElementById('sidebar-name').textContent = profile.full_name;
        }
    }

    async function loadAttendanceEvents() {
        const { data: regs } = await sb.from('event_registrations').select('event_id').eq('attendee_id', currentUserId).eq('status', 'approved');
        if (!regs || regs.length === 0) {
            document.getElementById('eventsContainer').innerHTML = '<p style="text-align:center; color:#64748b; padding: 40px;">No ongoing or completed events found.</p>';
            return;
        }
        
        const eventIds = regs.map(r => r.event_id);
        const { data: events } = await sb.from('events').select('*').in('id', eventIds);
        myEvents = events || [];
        renderEvents();
    }
    
    function getStoredCheckpoints(eventId) {
        const key = `chkpts_${currentUserId}_${eventId}`;
        const raw = localStorage.getItem(key);
        if (raw) return JSON.parse(raw);
        return [];
    }
    
    function saveCheckpoint(eventId, index) {
        const key = `chkpts_${currentUserId}_${eventId}`;
        let arr = getStoredCheckpoints(eventId);
        if (!arr.includes(index)) {
            arr.push(index);
            localStorage.setItem(key, JSON.stringify(arr));
            
            // Re-render UI to show new progress
            renderEvents();
            if (currentEventForLocation && currentEventForLocation.id === eventId) {
                // If timeline is open for this event, refresh it
                const ev = currentEventForLocation;
                const totalCp = ev.checkpoints_count || 4;
                const percent = Math.round((arr.length / totalCp) * 100);
                openTimeline(eventId, percent, arr.length, totalCp);
            }
        }
    }
    
    function startBackgroundTracker() {
        if (!navigator.geolocation) return;
        globalLocationWatchId = navigator.geolocation.watchPosition(pos => {
            lastKnownLat = pos.coords.latitude;
            lastKnownLng = pos.coords.longitude;
            locationActive = true;
            evaluateCheckpoints();
            if (document.getElementById('timelineModal').classList.contains('active')) {
                checkLocationUI();
            }
        }, err => {
            console.error("Location tracking error", err);
            locationActive = false;
        }, { enableHighAccuracy: true });
    }
    
    function getDistance(lat1, lon1, lat2, lon2) {
        if (!lat1 || !lon1 || !lat2 || !lon2) return 999999;
        const R = 6371e3; // metres
        const f1 = lat1 * Math.PI/180;
        const f2 = lat2 * Math.PI/180;
        const df = (lat2-lat1) * Math.PI/180;
        const dl = (lon2-lon1) * Math.PI/180;
        const a = Math.sin(df/2) * Math.sin(df/2) + Math.cos(f1) * Math.cos(f2) * Math.sin(dl/2) * Math.sin(dl/2);
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
        return Math.round(R * c);
    }
    
    function evaluateCheckpoints() {
        if (!locationActive) return;
        const now = new Date();
        
        myEvents.forEach(ev => {
            const start = new Date(ev.start_date + 'T' + (ev.start_time || '00:00:00'));
            const end = ev.end_date ? new Date(ev.end_date + 'T' + (ev.end_time || '23:59:59')) : new Date(start.getTime() + 7200000);
            
            if (now >= start && now <= end) {
                // Event is LIVE! Let's check location
                const demoEl = document.getElementById('demoOutside');
                const isDemoOutside = demoEl && demoEl.checked;
                let dist = getDistance(lastKnownLat, lastKnownLng, ev.latitude, ev.longitude);
                if (isDemoOutside) dist += (ev.attendance_radius_meters || 100) + 50;
                
                if (dist <= (ev.attendance_radius_meters || 100)) {
                    // Inside geofence! Calculate which checkpoint window we are in
                    const totalCp = ev.checkpoints_count || 4;
                    const durationMs = end.getTime() - start.getTime();
                    const windowMs = durationMs / totalCp;
                    
                    const elapsedMs = now.getTime() - start.getTime();
                    const currentWindowIndex = Math.floor(elapsedMs / windowMs);
                    
                    if (currentWindowIndex >= 0 && currentWindowIndex < totalCp) {
                        saveCheckpoint(ev.id, currentWindowIndex);
                    }
                }
            }
        });
    }

    function renderEvents() {
        const container = document.getElementById('eventsContainer');
        container.innerHTML = '';
        const now = new Date();

        myEvents.forEach(ev => {
            let start = new Date(ev.start_date + 'T' + (ev.start_time || '00:00:00'));
            let end = ev.end_date ? new Date(ev.end_date + 'T' + (ev.end_time || '23:59:59')) : new Date(start.getTime() + 7200000);
            
            if (now < start) return; // Hide upcoming

            const isLive = now >= start && now <= end;
            const statusBadge = isLive ? `<span class="status-badge status-live">Live now</span>` : `<span class="status-badge status-completed">Completed</span>`;
            
            const totalCp = ev.checkpoints_count || 4;
            const stored = getStoredCheckpoints(ev.id);
            const verifiedCp = stored.length;

            const percent = totalCp > 0 ? Math.round((verifiedCp / totalCp) * 100) : 0;
            const isVerifiedStatus = isLive ? `<span class="verification-status">🕒 Tracking Location...</span>` : `<span class="verification-status verified">✓ Finished</span>`;
            
            let cpsHtml = '';
            const durationMs = end.getTime() - start.getTime();
            const windowMs = durationMs / totalCp;
            
            for(let i=0; i<totalCp; i++) {
                const wStart = new Date(start.getTime() + (i * windowMs));
                const timeStr = wStart.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
                const name = `Checkpoint ${i+1}`;
                
                if (stored.includes(i)) {
                    cpsHtml += `<div class="checkpoint-item"><div class="cp-name">${timeStr} — ${name}</div><div class="cp-status verified">Verified ✓</div></div>`;
                } else {
                    cpsHtml += `<div class="checkpoint-item"><div class="cp-name">${timeStr} — ${name}</div><div class="cp-status">${isLive ? 'Pending GPS' : 'Missed'}</div></div>`;
                }
            }

            const card = document.createElement('div');
            card.className = 'event-card';
            card.innerHTML = `
                <div class="card-header">
                    ${statusBadge}
                    ${isVerifiedStatus}
                </div>
                <h2 class="event-title">${ev.title}</h2>
                <p class="event-meta">${ev.start_date || ''} · ${ev.venue_name || 'Online'}</p>
                
                <div class="progress-section">
                    <div class="progress-header"><span>Verified attendance</span><span>${percent}%</span></div>
                    <div class="progress-bar-bg"><div class="progress-bar-fill ${percent>=100?'complete':''}" style="width: ${percent}%"></div></div>
                </div>

                <div class="checkpoints-list">
                    ${cpsHtml}
                </div>

                <div class="card-actions">
                    <button class="btn-timeline" onclick="openTimeline('${ev.id}', ${percent}, ${verifiedCp}, ${totalCp})">Timeline</button>
                    <button class="btn-qr" onclick="openQR('${ev.id}', '${ev.title.replace(/'/g, "\\'")}', ${ev.qr_refresh_interval_sec || 60})">
                        <span style="font-size:20px">🔲</span> Attendance QR
                    </button>
                </div>
            `;
            container.appendChild(card);
        });
        
        if (container.innerHTML === '') {
            container.innerHTML = '<p style="text-align:center; color:#64748b; padding: 40px;">No ongoing or completed events found.</p>';
        }
    }

    function openTimeline(eventId, percent, verified, total) {
        const ev = myEvents.find(e => e.id === eventId);
        currentEventForLocation = ev;
        
        document.getElementById('tlPercent').textContent = percent + '%';
        document.getElementById('tlProgress').style.width = percent + '%';
        document.getElementById('tlProgress').className = percent >= 100 ? 'progress-bar-fill complete' : 'progress-bar-fill';
        document.getElementById('tlCount').textContent = `${verified} of ${total} checkpoints verified.`;
        
        const minReq = ev.min_attendance_percent || 80;
        document.getElementById('tlMinReq').textContent = `Minimum attendance requirement: ${minReq}%`;
        
        if (percent >= minReq) {
            document.getElementById('tlCertCard').style.background = '#f0fdf4';
            document.getElementById('tlCertCard').style.borderColor = '#d1fae5';
            document.getElementById('tlCertCard').innerHTML = `
                <div class="cert-title" style="color: #166534;">🎉 Certificate eligible!</div>
                <div class="cert-desc" style="color: #15803d; margin-bottom: 0;">You have met the ${minReq}% requirement.</div>
            `;
        } else {
            document.getElementById('tlCertCard').style.background = '#fffbeb';
            document.getElementById('tlCertCard').style.borderColor = '#fef3c7';
            document.getElementById('tlCertCard').innerHTML = `
                <div class="cert-title" style="color: #b45309;">⚠️ Certificate not eligible</div>
                <div class="cert-desc" style="color: #d97706; margin-bottom: 16px;" id="tlMinReq">Minimum attendance requirement: ${minReq}%</div>
                <button class="btn-cert">Reach ${minReq}% to unlock</button>
            `;
        }
        
        checkLocationUI();
        document.getElementById('timelineModal').classList.add('active');
    }

    function closeTimeline() {
        document.getElementById('timelineModal').classList.remove('active');
        currentEventForLocation = null;
    }

    function checkLocationUI() {
        const ev = currentEventForLocation;
        if (!ev) return;

        const card = document.getElementById('tlLocationCard');
        const title = document.getElementById('tlLocTitle');
        const desc = document.getElementById('tlLocDesc');
        const meta = document.getElementById('tlLocMeta');
        const dist = document.getElementById('tlLocDist');
        const icon = document.getElementById('tlLocIcon');

        meta.innerHTML = `📍 ${ev.venue_name || 'Event Venue'}<br>${ev.latitude || 0}, ${ev.longitude || 0} &nbsp; Radius: ${ev.attendance_radius_meters || 100}m`;

        if (!ev.latitude || !ev.longitude) {
            card.className = 'location-card invalid';
            title.innerHTML = 'Location not set';
            desc.innerHTML = 'The organizer has not set a physical location for this event.';
            dist.innerHTML = '';
            icon.innerHTML = '❌';
            return;
        }

        if (locationActive && lastKnownLat && lastKnownLng) {
            const isDemoOutside = document.getElementById('demoOutside').checked;
            let distance = getDistance(lastKnownLat, lastKnownLng, ev.latitude, ev.longitude);
            if (isDemoOutside) distance += (ev.attendance_radius_meters || 100) + 50;

            dist.innerHTML = `Your distance: ${distance} m`;

            if (distance <= (ev.attendance_radius_meters || 100)) {
                card.className = 'location-card';
                title.innerHTML = '✓ Location Verified';
                desc.innerHTML = "You're within the event attendance zone. Background tracker will log checkpoints automatically.";
                icon.innerHTML = '🎯';
            } else {
                card.className = 'location-card invalid';
                title.innerHTML = 'Outside Attendance Zone';
                desc.innerHTML = "You are too far from the event venue to mark attendance.";
                icon.innerHTML = '🚫';
            }
        } else {
            card.className = 'location-card invalid';
            title.innerHTML = 'Detecting Location...';
            desc.innerHTML = 'Please ensure location permissions are granted.';
            dist.innerHTML = '';
            icon.innerHTML = '🔒';
        }
    }
    
    // Wire up demo toggle to update UI and evaluate immediately
    window.onload = () => {
        const demo = document.getElementById('demoOutside');
        if (demo) demo.addEventListener('change', () => {
            checkLocationUI();
            evaluateCheckpoints();
        });
    };

    function openQR(eventId, title, refreshIntervalSec) {
        document.getElementById('qrEventName').textContent = title;
        document.getElementById('qrModal').classList.add('active');
        
        if (!qrcodeObj) {
            qrcodeObj = new QRCode(document.getElementById("qrcode"), {
                width: 250, height: 250, colorDark : "#0f172a", colorLight : "#ffffff", correctLevel : QRCode.CorrectLevel.H
            });
        }
        
        generateDynamicQR(eventId, refreshIntervalSec);
        qrInterval = setInterval(() => generateDynamicQR(eventId, refreshIntervalSec), refreshIntervalSec * 1000);
        
        let timeLeft = refreshIntervalSec;
        document.getElementById('qrTimeLeft').textContent = timeLeft;
        qrTimerInterval = setInterval(() => {
            timeLeft--;
            if (timeLeft <= 0) timeLeft = refreshIntervalSec;
            document.getElementById('qrTimeLeft').textContent = timeLeft;
        }, 1000);
    }

    function generateDynamicQR(eventId, refreshIntervalSec) {
        const windowMs = refreshIntervalSec * 1000;
        const timestamp = Math.floor(Date.now() / windowMs) * windowMs;
        const data = JSON.stringify({
            event_id: eventId,
            attendee_id: currentUserId,
            timestamp: timestamp
        });
        qrcodeObj.clear();
        qrcodeObj.makeCode(data);
    }

    function closeQR() {
        document.getElementById('qrModal').classList.remove('active');
        clearInterval(qrInterval);
        clearInterval(qrTimerInterval);
    }

    main();
</script>"""

new_content = re.sub(r'<script>.*?</script>', new_script, content, flags=re.DOTALL)

with open('attendee_attendance.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Done replacing script!")
