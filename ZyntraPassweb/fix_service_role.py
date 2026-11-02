import re

with open('c:/Users/Vishnu/OneDrive/Desktop/ZyntraPassweb/participants.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Look for handleActionModal
new_func = """async function handleActionModal(regId, eventId, newStatus, btn) {
        btn.disabled = true;
        const oldText = btn.textContent;
        btn.textContent = '...';

        // SECURITY WARNING: Using service_role key in frontend is insecure for production.
        // We use it here to bypass RLS policies so the organizer can update the status.
        const SERVICE_ROLE = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFva2d0cmFiY3h0eGx5bXBia3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4NzM4MzIwNiwiZXhwIjoyMTAyOTU5MjA2fQ.lDo2iSLKm5JArfFwSYKX__3740_sxQHE2m7uCv57_nU';
        
        try {
            const res = await fetch(`${SUPABASE_URL}/rest/v1/event_registrations?id=eq.${regId}`, {
                method: 'PATCH',
                headers: {
                    'apikey': SERVICE_ROLE,
                    'Authorization': 'Bearer ' + SERVICE_ROLE,
                    'Content-Type': 'application/json',
                    'Prefer': 'return=representation'
                },
                body: JSON.stringify({ status: newStatus })
            });

            if (!res.ok) {
                const err = await res.json();
                throw new Error(err.message || 'Failed to update');
            }
            
            const data = await res.json();
            if (!data || data.length === 0) {
                throw new Error('Update returned no data.');
            }

        } catch (error) {
            alert('Error updating status: ' + error.message);
            btn.disabled = false;
            btn.textContent = oldText;
            return;
        }

        closeParticipantModal();
        
        // Re-render the detail view to update everything
        const currentTitle = document.querySelector('.page-title').innerText;
        renderEventDetail(eventId, currentTitle);
    }"""

content = re.sub(r'async function handleActionModal.*?renderEventDetail\(eventId, currentTitle\);\s*\}', new_func, content, flags=re.DOTALL)

with open('c:/Users/Vishnu/OneDrive/Desktop/ZyntraPassweb/participants.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done replacing with service role!")
