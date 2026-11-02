let allEvents = [];
let currentFilter = 'all';
let supabase;

async function bootstrap() {
    try {
        const SUPABASE_URL = 'https://qokgtrabcxtxlympbkyb.supabase.co';
        const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFva2d0cmFiY3h0eGx5bXBia3liIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODczODMyMDYsImV4cCI6MjEwMjk1OTIwNn0.hbs5MZ4FiqUoZxDTrGqtMPOjRbbKUupgZOcoeLZa3ME';
        
        if (!window.supabase) {
            throw new Error("Supabase library not loaded. Check internet connection or adblockers.");
        }
        
        supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

        const { data: { session }, error } = await supabase.auth.getSession();
        if (error || !session) {
            window.location.href = 'index.html';
            return;
        }
        
        // Set Avatar initials
        const { data: profile, error: profError } = await supabase.from('profiles').select('full_name').eq('id', session.user.id).maybeSingle();
        if (profile && profile.full_name) {
            const initials = profile.full_name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
            
            const userAvatar = document.getElementById('userAvatar');
            if(userAvatar) userAvatar.textContent = initials;
            
            const sidebarAvatar = document.getElementById('sidebar-avatar');
            if(sidebarAvatar) sidebarAvatar.textContent = initials;
            
            const sidebarName = document.getElementById('sidebar-name');
            if(sidebarName) sidebarName.textContent = profile.full_name;
        }
        
        const sidebarEmail = document.getElementById('sidebar-email');
        if(sidebarEmail) sidebarEmail.textContent = session.user.email;

        // Sidebar Toggle Logic
        const sidebar = document.getElementById('sidebar');
        const overlay = document.getElementById('sidebar-overlay');
        const menuBtn = document.querySelector('.btn-menu');
        
        if (menuBtn && sidebar && overlay) {
            menuBtn.addEventListener('click', () => {
                sidebar.classList.add('active');
                overlay.classList.add('active');
            });
            overlay.addEventListener('click', () => {
                sidebar.classList.remove('active');
                overlay.classList.remove('active');
            });
        }

        const logoutBtn = document.getElementById('sidebar-logout');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', async () => {
                await supabase.auth.signOut();
                window.location.href = 'index.html';
            });
        }

        await fetchEvents(session.user.id);
        
        // Tab Switching
        document.querySelectorAll('.tab').forEach(tab => {
            tab.addEventListener('click', (e) => {
                document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
                e.currentTarget.classList.add('active');
                currentFilter = e.currentTarget.dataset.filter;
                renderEvents();
            });
        });

    } catch (err) {
        document.getElementById('events-feed').innerHTML = `<p style="text-align: center; color: red; padding: 20px;"><b>Startup Error:</b> ${err.message}</p>`;
        console.error(err);
    }
}

async function fetchEvents(userId) {
    try {
        const { data, error } = await supabase
            .from('events')
            .select('*')
            .eq('organizer_id', userId)
            .order('created_at', { ascending: false });

        if (error) {
            document.getElementById('events-feed').innerHTML = `<p style="text-align: center; color: red; padding: 20px;"><b>Database Error:</b> ${error.message}</p>`;
            return;
        }

        allEvents = data || [];
        updateBadges();
        renderEvents();
    } catch (err) {
        document.getElementById('events-feed').innerHTML = `<p style="text-align: center; color: red; padding: 20px;"><b>Fetch Error:</b> ${err.message}</p>`;
    }
}

function updateBadges() {
    const counts = { all: allEvents.length, upcoming: 0, ongoing: 0, completed: 0, cancelled: 0 };
    allEvents.forEach(ev => {
        const status = (ev.status || 'upcoming').toLowerCase();
        if (counts[status] !== undefined) counts[status]++;
    });

    const bAll = document.getElementById('badge-all'); if(bAll) bAll.textContent = counts.all;
    const bUpcoming = document.getElementById('badge-upcoming'); if(bUpcoming) bUpcoming.textContent = counts.upcoming;
    const bOngoing = document.getElementById('badge-ongoing'); if(bOngoing) bOngoing.textContent = counts.ongoing;
    const bCompleted = document.getElementById('badge-completed'); if(bCompleted) bCompleted.textContent = counts.completed;
    const bCancelled = document.getElementById('badge-cancelled'); if(bCancelled) bCancelled.textContent = counts.cancelled;
}

function renderEvents() {
    const feed = document.getElementById('events-feed');
    if (!feed) return;
    
    feed.innerHTML = '';

    const filtered = allEvents.filter(ev => {
        if (currentFilter === 'all') return true;
        const status = (ev.status || 'upcoming').toLowerCase();
        return status === currentFilter;
    });

    if (filtered.length === 0) {
        feed.innerHTML = `<p style="text-align: center; color: #64748b; margin-top: 40px;">No events found in this category.</p>`;
        return;
    }

    filtered.forEach(ev => {
        const status = (ev.status || 'upcoming').toLowerCase();
        const bannerUrl = ev.banner_image_url || 'https://via.placeholder.com/600x300?text=No+Image';
        const title = ev.title || 'Untitled event';
        const category = ev.category || 'Event';
        const checkpoints = ev.checkpoints_count ? `${ev.checkpoints_count} checkpoints` : '0 checkpoints';

        const card = document.createElement('div');
        card.className = 'event-card';
        card.innerHTML = `
            <img src="${bannerUrl}" alt="Event Banner" class="event-banner" onerror="this.src='https://via.placeholder.com/600x300?text=No+Image'">
            <div class="event-tags">
                <span class="tag tag-status">${status}</span>
                <span class="tag tag-category">${category}</span>
                <span class="tag tag-checkpoints">${checkpoints}</span>
            </div>
            <h3 class="event-title">${title}</h3>
        `;
        feed.appendChild(card);
    });
}

// Ensure elements are ready before we execute
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bootstrap);
} else {
    bootstrap();
}
