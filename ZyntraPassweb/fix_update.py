import re

with open('c:/Users/Vishnu/OneDrive/Desktop/ZyntraPassweb/participants.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add cache buster to renderEventDetail
content = re.sub(
    r'(\$\{SUPABASE_URL\}/rest/v1/event_registrations\?event_id=eq\.\$\{eventId\}&select=\*&order=created_at\.asc)',
    r'\1&_cb=${Date.now()}',
    content
)

# Update handleActionModal to check for RLS failure
new_func = """async function handleActionModal(regId, eventId, newStatus, btn) {
        btn.disabled = true;
        const oldText = btn.textContent;
        btn.textContent = '...';

        const { data, error } = await sb
            .from('event_registrations')
            .update({ status: newStatus })
            .eq('id', regId)
            .select();

        if (error) {
            alert('Error updating status: ' + error.message);
            btn.disabled = false;
            btn.textContent = oldText;
            return;
        }

        if (!data || data.length === 0) {
            alert('Update failed! You might not have permission to update this record.');
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

print("Done")
