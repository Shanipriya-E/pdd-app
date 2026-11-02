import re

with open('c:/Users/Vishnu/OneDrive/Desktop/ZyntraPassweb/attendee_attendance.html', 'r', encoding='utf-8') as f:
    content = f.read()

replacement = """    async function saveCheckpoint(eventId, index) {
        const key = `chkpts_${currentUserId}_${eventId}`;
        let arr = getStoredCheckpoints(eventId);
        if (!arr.includes(index)) {
            arr.push(index);
            localStorage.setItem(key, JSON.stringify(arr));
            
            // Try to sync to Supabase
            try {
                await sb.from('attendance_logs').insert([{
                    event_id: eventId,
                    attendee_id: currentUserId,
                    checkpoint_index: index,
                    latitude: lastKnownLat,
                    longitude: lastKnownLng
                }]);
            } catch (e) { console.error("Sync error:", e); }
            
            // Update UI if timeline open
            if (currentEventForLocation && currentEventForLocation.id === eventId) {
                const ev = currentEventForLocation;
                const totalCp = ev.checkpoints_count || 4;
                const percent = Math.round((arr.length / totalCp) * 100);
                openTimeline(eventId, percent, arr.length, totalCp);
            }
        }
    }"""

content = re.sub(r'\s*function saveCheckpoint\(eventId, index\).*?\}\s*\}', '\n\n' + replacement, content, flags=re.DOTALL)

with open('c:/Users/Vishnu/OneDrive/Desktop/ZyntraPassweb/attendee_attendance.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated attendee_attendance.html to sync with Supabase!")
