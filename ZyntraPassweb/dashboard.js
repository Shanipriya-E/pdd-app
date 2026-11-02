document.addEventListener('DOMContentLoaded', async () => {
    let supabase;
    try {
        const supabaseUrl = 'https://qokgtrabcxtxlympbkyb.supabase.co';
        const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFva2d0cmFiY3h0eGx5bXBia3liIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODczODMyMDYsImV4cCI6MjEwMjk1OTIwNn0.hbs5MZ4FiqUoZxDTrGqtMPOjRbbKUupgZOcoeLZa3ME';
        if (window.supabase) {
            supabase = window.supabase.createClient(supabaseUrl, supabaseKey);
        }
    } catch (e) {
        console.error("Supabase init error:", e);
        return;
    }

    if (!supabase) {
        alert("Database connection not ready.");
        return;
    }

    const loadingState = document.getElementById('loading-state');
    const dashboardContent = document.getElementById('dashboard-content');

    try {
        // 1. Check if user is logged in
        const { data: { session }, error: sessionError } = await supabase.auth.getSession();
        
        if (sessionError || !session) {
            // Redirect to login if not authenticated
            window.location.href = 'login.html';
            return;
        }

        const user = session.user;

        // 2. Fetch Organizer Profile Data
        const { data: profile, error: profileError } = await supabase
            .from('profiles')
            .select('*')
            .eq('id', user.id)
            .single();

        if (profileError) throw profileError;

        // Verify role
        if (profile.role !== 'organizer') {
            alert("Access Denied: You are not an Organizer.");
            window.location.href = 'login.html';
            return;
        }

        // Sidebar Toggle Logic
        const menuBtn = document.querySelector('.menu-btn');
        const sidebar = document.getElementById('sidebar');
        const overlay = document.getElementById('sidebar-overlay');

        menuBtn.addEventListener('click', () => {
            sidebar.classList.add('active');
            overlay.classList.add('active');
        });

        overlay.addEventListener('click', () => {
            sidebar.classList.remove('active');
            overlay.classList.remove('active');
        });
        
        document.getElementById('sidebar-logout').addEventListener('click', async () => {
            await supabase.auth.signOut();
            window.location.href = 'login.html';
        });

        // 3. Update Greeting UI
        document.getElementById('greeting-text').textContent = `Good evening, ${profile.full_name}`;
        
        // Use initials for avatar
        const initials = profile.full_name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
        const el = document.getElementById('profile-avatar');
        if (el) el.textContent = initials;
        
        // Populate Sidebar Profile
        document.getElementById('sidebar-avatar').textContent = initials;
        document.getElementById('sidebar-name').textContent = profile.full_name;
        document.getElementById('sidebar-email').textContent = user.email;

        // 4. Fetch Real Stats
        // Events
        const { count: totalEvents, error: eventsErr } = await supabase
            .from('events')
            .select('*', { count: 'exact', head: true })
            .eq('organizer_id', profile.id);
            
        // For the sake of the dashboard UI, let's just query all registrations tied to their events.
        // We'll use a direct count from event_registrations (RLS policy already filters by organizer's events).
        // Count ALL registrations (registered + approved + attended — excludes rejected)
        const { count: totalRegs, error: regsErr } = await supabase
            .from('event_registrations')
            .select('*', { count: 'exact', head: true })
            .in('status', ['registered', 'approved', 'attended']);

        // Verified = attended (checked-in)
        const { count: verifiedRegs, error: verErr } = await supabase
            .from('event_registrations')
            .select('*', { count: 'exact', head: true })
            .eq('status', 'attended');

        // Pending = still waiting for organizer review
        const { count: pendingRegs, error: pendErr } = await supabase
            .from('event_registrations')
            .select('*', { count: 'exact', head: true })
            .eq('status', 'registered');

        const { count: totalCerts, error: certsErr } = await supabase
            .from('certificates')
            .select('*', { count: 'exact', head: true });

        // Update Subtitle
        const eventCount = totalEvents || 0;
        document.getElementById('greeting-subtext').textContent = 
            `${profile.institution} · ${profile.area_city} · ${eventCount} events`;

        // Update Stat Cards
        document.getElementById('stat-total-events').textContent = eventCount;
        document.getElementById('stat-sub-events').textContent = `${eventCount} upcoming`;
        
        document.getElementById('stat-registrations').textContent = (totalRegs || 0).toLocaleString();
        document.getElementById('stat-verified').textContent = (verifiedRegs || 0).toLocaleString();
        document.getElementById('stat-pending').textContent = (pendingRegs || 0).toLocaleString();
        document.getElementById('stat-certificates').textContent = (totalCerts || 0).toLocaleString();

        // Reveal Dashboard
        loadingState.style.display = 'none';
        dashboardContent.style.display = 'block';

    } catch (error) {
        console.error("Error loading dashboard:", error.message);
        loadingState.textContent = "Error loading dashboard: " + error.message;
    }
});
