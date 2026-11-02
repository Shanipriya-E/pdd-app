# -*- coding: utf-8 -*-
with open('attendee_certificates.html', 'w', encoding='utf-8') as f:
    f.write(r'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZyntraPass - My Certificates</title>
    <!-- Supabase SDK -->
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
        body { background-color: #f7f9fc; color: #0d162a; padding-bottom: 70px; }
        
        .top-bar { background-color: white; padding: 16px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #e2e8f0; position: sticky; top: 0; z-index: 100; }
        .btn-menu { background: white; border: 1px solid #e2e8f0; border-radius: 12px; width: 44px; height: 44px; font-size: 20px; cursor: pointer; color: #0d162a; }
        
        .container { padding: 24px; max-width: 800px; margin: 0 auto; }
        .page-title { font-size: 28px; font-weight: 800; color: #0f172a; margin-bottom: 8px; }
        .subtitle { font-size: 15px; color: #475569; line-height: 1.5; margin-bottom: 24px; }
        
        .cert-card { background: white; border: 1px solid #e2e8f0; border-radius: 16px; padding: 20px; cursor: pointer; transition: transform 0.2s, box-shadow 0.2s; }
        .cert-card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.05); border-color: #cbd5e1; }
        .cert-card h3 { font-size: 18px; color: #0f172a; margin-bottom: 8px; }
        .cert-card p { font-size: 14px; color: #64748b; margin-bottom:0; }

        .modal-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); z-index: 1000; display: none; align-items: center; justify-content: center; }
        .modal-overlay.active { display: flex; }
        .modal-content { background: white; border-radius: 16px; width: 95%; max-width: 800px; padding: 24px; position: relative; max-height: 95vh; overflow-y: auto; }
        
        .btn-create { background-color: #5b54e3; color: white; border: none; border-radius: 12px; padding: 14px 24px; font-weight: 600; font-size: 15px; cursor: pointer; display: inline-flex; align-items: center; justify-content: center; gap: 8px; margin-top: 16px;}
        .btn-create:hover { background-color: #4a44b8; }
        
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
                <p class="sidebar-subbrand">Attendee workspace</p>
            </div>
        </div>
        <div class="sidebar-menu">
            <a href="attendee_dashboard.html" class="sidebar-item"><span>🏠</span> Discover</a>
            <a href="attendee_events.html" class="sidebar-item"><span>📅</span> My Events</a>
            <a href="attendee_certificates.html" class="sidebar-item active"><span>📜</span> Certificates</a>
            <a href="attendee_settings.html" class="sidebar-item"><span>⚙️</span> Settings</a>
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
        <h1 class="page-title">My Certificates</h1>
        <p class="subtitle">View and download your earned certificates.</p>

        <div id="certs-list" style="display: flex; flex-direction: column; gap: 16px; margin-top: 24px;">
            <p>Loading your certificates...</p>
        </div>

        <div class="modal-overlay" id="cert-modal">
            <div class="modal-content">
                <button onclick="document.getElementById('cert-modal').classList.remove('active')" style="position:absolute; right:20px; top:20px; background:white; border-radius:50%; width:36px; height:36px; border:1px solid #e2e8f0; font-size:20px; cursor:pointer; z-index: 10;">&#215;</button>
                <h2 id="modal-event-title" style="margin-bottom: 24px;">Event Title</h2>
                
                <!-- Canvas for dynamic rendering -->
                <div style="width:100%; overflow:auto; text-align:center; background:#f1f5f9; padding:16px; border-radius:12px;">
                    <canvas id="cert-canvas" style="max-width: 100%; height: auto; box-shadow: 0 4px 12px rgba(0,0,0,0.1); display:none;"></canvas>
                    <p id="canvas-loading">Rendering your certificate...</p>
                </div>
                
                <button id="btn-download" class="btn-create" style="width: 100%; display:none;">Download Certificate</button>
            </div>
        </div>
    </div>

<script>
    const SUPABASE_URL  = 'https://qokgtrabcxtxlympbkyb.supabase.co';
    const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFva2d0cmFiY3h0eGx5bXBia3liIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODczODMyMDYsImV4cCI6MjEwMjk1OTIwNn0.hbs5MZ4FiqUoZxDTrGqtMPOjRbbKUupgZOcoeLZa3ME';

    let sb, currentUserId, currentUserEmail;
    let currentUserName = "Attendee";
    let canvasBlob = null;

    async function main() {
        sb = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
        const { data: { session } } = await sb.auth.getSession();
        if (!session) { window.location.href = 'index.html'; return; }
        
        currentUserId = session.user.id;
        currentUserEmail = session.user.email;
        
        document.getElementById('sidebar-email').textContent = currentUserEmail;
        const sidebar = document.getElementById('sidebar');
        const overlay = document.getElementById('sidebar-overlay');
        document.getElementById('menuBtn').addEventListener('click', () => { sidebar.classList.add('active'); overlay.classList.add('active'); });
        overlay.addEventListener('click', () => { sidebar.classList.remove('active'); overlay.classList.remove('active'); });
        
        const logoutHandler = async () => { await sb.auth.signOut(); window.location.href = 'index.html'; };
        document.getElementById('sidebar-logout').addEventListener('click', logoutHandler);
        
        const { data: profile } = await sb.from('profiles').select('*').eq('id', currentUserId).maybeSingle();
        if (profile && profile.full_name) {
            currentUserName = profile.full_name;
            const initials = profile.full_name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
            document.getElementById('sidebar-avatar').textContent = initials;
            document.getElementById('sidebar-name').textContent   = profile.full_name;
        }

        loadMyCerts();
        
        document.getElementById('btn-download').addEventListener('click', downloadCertificate);
    }

    async function loadMyCerts() {
        const listDiv = document.getElementById('certs-list');
        listDiv.innerHTML = '<p>Loading...</p>';
        
        const { data: certs, error } = await sb.from('certificates').select('*, events(title, certificate_template_url)').eq('attendee_id', currentUserId);
            
        if (error) {
            console.error(error);
            listDiv.innerHTML = '<p style="color:red">Failed to load certificates.</p>';
            return;
        }
        
        if (!certs || certs.length === 0) {
            listDiv.innerHTML = '<p style="color:#64748b;">You have not earned any certificates yet. Attend events and meet the 80% attendance requirement to earn them!</p>';
            return;
        }
        
        listDiv.innerHTML = '';
        certs.forEach(cert => {
            const ev = cert.events || {};
            const card = document.createElement('div');
            card.className = 'cert-card';
            card.innerHTML = `
                <h3>${ev.title || 'Event Certificate'}</h3>
                <p>Issued on ${new Date(cert.issued_at).toLocaleDateString()}</p>
                <span style="display:inline-block; margin-top:8px; background:#dcfce7; color:#166534; padding:2px 8px; border-radius:12px; font-size:12px; font-weight:600;">Verified</span>
            `;
            card.onclick = () => openCertModal(ev);
            listDiv.appendChild(card);
        });
    }

    function openCertModal(ev) {
        document.getElementById('modal-event-title').textContent = ev.title;
        document.getElementById('cert-modal').classList.add('active');
        
        const canvas = document.getElementById('cert-canvas');
        const loading = document.getElementById('canvas-loading');
        const btn = document.getElementById('btn-download');
        
        canvas.style.display = 'none';
        btn.style.display = 'none';
        loading.style.display = 'block';
        
        const img = new Image();
        img.crossOrigin = "Anonymous";
        img.onload = () => {
            canvas.width = img.width;
            canvas.height = img.height;
            const ctx = canvas.getContext('2d');
            
            // Draw template
            ctx.drawImage(img, 0, 0);
            
            // Render Name
            ctx.fillStyle = "#000000";
            ctx.textAlign = "center";
            ctx.textBaseline = "middle";
            ctx.font = `bold ${Math.floor(canvas.height * 0.08)}px "Segoe UI", Arial`;
            
            ctx.fillText(currentUserName, canvas.width / 2, canvas.height / 2);
            
            canvas.toBlob((blob) => {
                canvasBlob = blob;
                loading.style.display = 'none';
                canvas.style.display = 'block';
                btn.style.display = 'block';
            }, 'image/png');
        };
        img.onerror = () => {
            loading.textContent = "Error loading certificate template.";
            loading.style.color = "red";
        };
        img.src = ev.certificate_template_url;
    }

    function downloadCertificate() {
        if (!canvasBlob) return;
        const url = URL.createObjectURL(canvasBlob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `Certificate_${currentUserName.replace(/\s+/g, '_')}.png`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    main();
</script>
</body>
</html>'''
    )
