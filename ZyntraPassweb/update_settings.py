import re

files = ['c:/Users/Vishnu/OneDrive/Desktop/ZyntraPassweb/settings.html', 'c:/Users/Vishnu/OneDrive/Desktop/ZyntraPassweb/attendee_settings.html']

password_old = r'<form id="password-form">.*?</form>'
password_new = '''<form id="password-form">
                <div class="form-group">
                    <label class="form-label">Current password</label>
                    <input type="password" class="form-input" id="inp-current-pass" required>
                </div>
                <div class="form-group">
                    <label class="form-label">New password</label>
                    <input type="password" class="form-input" id="inp-new-pass" required minlength="6">
                </div>
                <div style="text-align: right; margin-bottom: 16px;">
                    <a href="javascript:alert(\'Forgot Password flow will be sent to your email!\')" style="color: #5b54e3; font-size: 13px; text-decoration: none; font-weight: 600;">Forgot password?</a>
                </div>
                <button type="submit" class="btn-primary" id="btn-save-password">Update password</button>
                <div class="success-msg" id="msg-pwd-success">Password updated successfully.</div>
                <div class="error-msg" id="msg-pwd-error">Error updating password.</div>
            </form>'''

privacy_old = r'<div class="tab-content" id="tab-privacy">\s*<div class="settings-card">\s*<h2 class="card-title">Privacy</h2>\s*<p class="card-desc">Privacy settings will be available in the next update.</p>\s*</div>\s*</div>'
privacy_new = '''<div class="tab-content" id="tab-privacy">
        <div class="settings-card">
            <h2 class="card-title">Privacy and Policy</h2>
            <p class="card-desc" style="margin-bottom: 12px;">Here are our core privacy principles:</p>
            <ul style="margin-left: 20px; color: #475569; font-size: 14px; line-height: 1.8;">
                <li><strong>1. Data Minimization:</strong> We only collect the personal data absolutely necessary to provide our event management services.</li>
                <li><strong>2. Secure Storage:</strong> Your information is encrypted in transit and at rest using industry-standard security measures.</li>
                <li><strong>3. No Third-Party Selling:</strong> We never sell your personal information or attendee data to third-party marketers or advertisers.</li>
                <li><strong>4. User Control:</strong> You have the right to access, modify, or permanently delete your account data at any time.</li>
                <li><strong>5. Transparent Tracking:</strong> We only use essential cookies and tracking for functionality, not for invasive cross-site profiling.</li>
            </ul>
        </div>
    </div>'''

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Replace Password form
    content = re.sub(password_old, password_new, content, flags=re.DOTALL)
    
    # Replace Privacy content
    content = re.sub(privacy_old, privacy_new, content, flags=re.DOTALL)
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

print("Updated Settings files")
