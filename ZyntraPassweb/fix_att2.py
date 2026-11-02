import os

app_dir = r"C:\Users\Vishnu\zyntraPassForntend\app\src\main"
java_dir = os.path.join(app_dir, r"java\com\simats\zyntrapass")

with open(os.path.join(java_dir, 'AttendeeCertificatesActivity.kt'), 'r', encoding='utf-8') as f:
    content = f.read()
    
# Let's just blindly replace the incorrect URL part if it exists
import re
content = re.sub(r'SupabaseApi\.get\("rest/v1/certificates\?attendee_id=eq\..*?select=\*,events\(title,certificate_template_url\)"\)',
                 r'SupabaseApi.get("rest/v1/certificates?attendee_id=eq.&select=*,events(title,certificate_template_url)")',
                 content)

with open(os.path.join(java_dir, 'AttendeeCertificatesActivity.kt'), 'w', encoding='utf-8') as f:
    f.write(content)
