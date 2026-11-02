# -*- coding: utf-8 -*-
import re

with open('attendee_dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix active state in sidebar
html = html.replace('href="attendee_dashboard.html" class="sidebar-item active"', 'href="attendee_dashboard.html" class="sidebar-item"')
html = html.replace('<div class="sidebar-menu">', '<div class="sidebar-menu">\n        <a href="attendee_certificates.html" class="sidebar-item active"><span>??</span> Certificates</a>')

# Same for bottom nav
html = html.replace('href="attendee_dashboard.html" class="nav-item active"', 'href="attendee_dashboard.html" class="nav-item"')
html = html.replace('<!-- ?? Bottom Nav ?? -->\n<div class="bottom-nav">', '<!-- ?? Bottom Nav ?? -->\n<div class="bottom-nav">\n    <a href="attendee_certificates.html" class="nav-item active"><span class="nav-icon">??</span><span>Certificates</span></a>')


# Replace container content
main_content = '''<div class="container" style="max-width: 800px;">
    <h1 style="font-size: 28px; font-weight: 800; color: #0f172a; margin-bottom: 8px;">My Certificates</h1>
    <p class="subtitle">View and download your earned event certificates.</p>

    <!-- Cert List -->
    <div id="certs-list" style="display: flex; flex-direction: column; gap: 16px; margin-top: 24px;">
        <p>Loading your certificates...</p>
    </div>

    <!-- Canvas Modal -->
    <div class="modal-overlay" id="cert-modal">
        <div class="modal-content" style="max-width: 800px; width: 95%; padding: 24px; position:relative; text-align: center;">
            <button onclick="document.getElementById('cert-modal').classList.remove('active')" style="position:absolute; right:20px; top:20px; background:none; border:none; font-size:24px; cursor:pointer;">&#215;</button>
            <h2 id="modal-event-title" style="margin-bottom: 16px;">Event Certificate</h2>
            
            <div style="width: 100%; overflow: auto; margin-bottom: 16px; border: 1px solid #e2e8f0; border-radius: 8px;">
                <canvas id="cert-canvas" style="max-width: 100%; height: auto; display: block; margin: 0 auto;"></canvas>
            </div>

            <button id="btn-download" class="btn-create" style="width: 100%; padding:12px; font-size:16px;">Download Certificate</button>
        </div>
    </div>
</div>
'''

html = re.sub(r'<div class="container">.*?<!-- ?? Bottom Nav ?? -->', main_content + '\n<!-- ?? Bottom Nav ?? -->', html, flags=re.DOTALL)

# Inject CSS for Modal
css_inject = '''
        .modal-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); z-index: 1000; display: none; align-items: center; justify-content: center; }
        .modal-overlay.active { display: flex; }
        .modal-content { background: white; border-radius: 16px; position: relative; }
        
        .cert-card { background: white; border: 1px solid #e2e8f0; border-radius: 16px; padding: 20px; cursor: pointer; transition: transform 0.2s, box-shadow 0.2s; display: flex; align-items: center; justify-content: space-between; }
        .cert-card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.05); border-color: #cbd5e1; }
        .cert-card h3 { font-size: 18px; color: #0f172a; margin-bottom: 4px; }
        .cert-card p { font-size: 14px; color: #64748b; margin-bottom:0; }
'''
html = html.replace('</style>', css_inject + '\n    </style>')

# Replace the main() function logic
script_logic = '''
    let currentUserName = "Attendee";
    let canvasBlob = null;

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
            currentUserName = profile.full_name;
            const initials = profile.full_name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
            document.getElementById('sidebar-avatar').textContent = initials;
            document.getElementById('sidebar-name').textContent   = profile.full_name;
        }

        loadCertificates();
        
        document.getElementById('btn-download').addEventListener('click', () => {
            if (!canvasBlob) return;
            const url = URL.createObjectURL(canvasBlob);
            const a = document.createElement('a');
            a.href = url;
            a.download = "ZyntraPass_Certificate.png";
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        });
    }

    async function loadCertificates() {
        const listDiv = document.getElementById('certs-list');
        listDiv.innerHTML = '<p>Loading...</p>';
        
        const { data: certs, error } = await sb.from('certificates').select('*, events(title, certificate_template_url)').eq('attendee_id', currentUserId);
            
        if (error) {
            listDiv.innerHTML = '<p style="color:red">Failed to load certificates.</p>';
            return;
        }
        
        if (!certs || certs.length === 0) {
            listDiv.innerHTML = '<p style="color:#64748b;">You have not earned any certificates yet. Attend events and meet the 80% attendance requirement to earn them!</p>';
            return;
        }
        
        listDiv.innerHTML = '';
        certs.forEach(c => {
            const ev = c.events;
            const card = document.createElement('div');
            card.className = 'cert-card';
            card.innerHTML = 
                <div>
                    <h3></h3>
                    <p>Issued on: </p>
                </div>
                <div style="font-size:24px;">??</div>
            ;
            card.onclick = () => renderCertificate(ev);
            listDiv.appendChild(card);
        });
    }

    function renderCertificate(ev) {
        document.getElementById('modal-event-title').textContent = ev.title + " - Certificate";
        document.getElementById('cert-modal').classList.add('active');
        
        const canvas = document.getElementById('cert-canvas');
        const ctx = canvas.getContext('2d');
        
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        canvasBlob = null;
        
        if (!ev.certificate_template_url) {
            ctx.fillText("No template uploaded by organizer.", 50, 50);
            return;
        }

        const img = new Image();
        img.crossOrigin = "Anonymous";
        img.onload = () => {
            canvas.width = img.width;
            canvas.height = img.height;
            ctx.drawImage(img, 0, 0);
            
            // Draw Name Centered
            ctx.fillStyle = "#000000";
            ctx.textAlign = "center";
            ctx.textBaseline = "middle";
            // Responsive font size based on image height
            const fontSize = Math.floor(img.height * 0.08); 
            ctx.font = old px serif;
            
            ctx.fillText(currentUserName, img.width / 2, img.height / 2);
            
            canvas.toBlob((blob) => {
                canvasBlob = blob;
            }, 'image/png');
        };
        img.src = ev.certificate_template_url;
    }
'''

html = re.sub(r'async function main\(\) \{.*', script_logic + '\nmain();\n</script>\n</body>\n</html>', html, flags=re.DOTALL)

with open('attendee_certificates.html', 'w', encoding='utf-8') as f:
    f.write(html)
