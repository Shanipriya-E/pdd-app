# -*- coding: utf-8 -*-
with open('attendee_certificates.html', 'r', encoding='utf-8') as f:
    html = f.read()

bottom_nav_css = '''
        /* Bottom Nav */
        .bottom-nav {
            position: fixed; bottom: 0; left: 0; right: 0; background: white; border-top: 1px solid #e2e8f0; display: flex; justify-content: space-around; padding: 12px 0; z-index: 100;
        }
        .nav-item {
            display: flex; flex-direction: column; align-items: center; color: #64748b; font-size: 12px; font-weight: 500; cursor: pointer; text-decoration: none; gap: 4px;
        }
        .nav-item.active { color: #3b35a8; }
        .nav-icon { font-size: 20px; }
'''

if '.bottom-nav {' not in html:
    html = html.replace('</style>', bottom_nav_css + '\n    </style>')
    with open('attendee_certificates.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Added bottom-nav CSS")
else:
    print("CSS already present")
