import os

app_dir = r"C:\Users\Vishnu\zyntraPassForntend\app\src\main"
java_dir = os.path.join(app_dir, r"java\com\simats\zyntrapass")

with open(os.path.join(java_dir, 'AttendeeCertificatesActivity.kt'), 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'SupabaseApi.get("rest/v1/certificates?attendee_id=eq.&select=*,events(title,certificate_template_url)")',
    'SupabaseApi.get("rest/v1/certificates?attendee_id=eq.&select=*,events(title,certificate_template_url)")'
)

with open(os.path.join(java_dir, 'AttendeeCertificatesActivity.kt'), 'w', encoding='utf-8') as f:
    f.write(content)
