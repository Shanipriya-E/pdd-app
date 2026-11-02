import re

with open('c:/Users/Vishnu/OneDrive/Desktop/ZyntraPassweb/live.html', 'r', encoding='utf-8') as f:
    content = f.read()

replacement = """        // Fetch profiles
        const uids = regs.map(r => `"${r.attendee_id}"`).join(',');
        const pRes = await fetch(`${SUPABASE_URL}/rest/v1/profiles?id=in.(${uids})&select=id,full_name,email`, {
            headers: { 'apikey': SUPABASE_ANON, 'Authorization': 'Bearer ' + accessToken }
        });
        const profiles = await pRes.json();
        if (Array.isArray(profiles)) {
            profiles.forEach(p => profileMap[p.id] = p);
        }
        
        // Also fetch from attendee_profiles in case they are there
        const apRes = await fetch(`${SUPABASE_URL}/rest/v1/attendee_profiles?id=in.(${uids})&select=*`, {
            headers: { 'apikey': SUPABASE_ANON, 'Authorization': 'Bearer ' + accessToken }
        });
        const aProfiles = await apRes.json();
        if (Array.isArray(aProfiles)) {
            aProfiles.forEach(p => {
                if (!profileMap[p.id] || !profileMap[p.id].full_name) {
                    profileMap[p.id] = { ...(profileMap[p.id] || {}), ...p };
                }
            });
        }"""

content = re.sub(r'// Fetch profiles.*?\}\s*\}', replacement, content, flags=re.DOTALL)

with open('c:/Users/Vishnu/OneDrive/Desktop/ZyntraPassweb/live.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed profile fetching!")
