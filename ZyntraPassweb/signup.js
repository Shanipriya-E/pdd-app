document.addEventListener('DOMContentLoaded', () => {
    let supabase;
    try {
        const supabaseUrl = 'https://qokgtrabcxtxlympbkyb.supabase.co';
        const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFva2d0cmFiY3h0eGx5bXBia3liIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODczODMyMDYsImV4cCI6MjEwMjk1OTIwNn0.hbs5MZ4FiqUoZxDTrGqtMPOjRbbKUupgZOcoeLZa3ME';
        if (window.supabase) {
            supabase = window.supabase.createClient(supabaseUrl, supabaseKey);
        }
    } catch (e) {
        console.error("Supabase init error:", e);
    }

    // ── Security helpers ────────────────────────────────────────────────────
    // VULN-002 FIX: Strict role allowlist — URL param cannot grant elevated roles
    const ALLOWED_SIGNUP_ROLES = ['attendee', 'organizer'];

    // VULN-003 FIX: Input max-length validation
    const MAX_LENGTHS = { fullName: 100, institution: 200, areaCity: 100, nativePlace: 100 };
    function validateLength(value, field) {
        const max = MAX_LENGTHS[field] || 500;
        if (value.trim().length === 0) throw new Error(`${field} cannot be empty.`);
        if (value.length > max) throw new Error(`${field} must be under ${max} characters.`);
        return value.trim();
    }

    // VULN-018 FIX: Password strength enforcement
    function validatePasswordStrength(password) {
        const checks = {
            'at least 8 characters':    password.length >= 8,
            'an uppercase letter':       /[A-Z]/.test(password),
            'a lowercase letter':        /[a-z]/.test(password),
            'a number':                  /\d/.test(password),
        };
        const failed = Object.entries(checks).filter(([, ok]) => !ok).map(([rule]) => rule);
        if (failed.length > 0) {
            throw new Error('Password must include: ' + failed.join(', ') + '.');
        }
    }

    const signupForm = document.getElementById('signup-form');
    if (signupForm) {
        signupForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            if (!supabase) {
                alert("Database connection not ready. Try running on a local server instead of file://");
                return;
            }

            const fullName = document.getElementById('fullName').value;
            const email = document.getElementById('email').value;
            const phone = document.getElementById('phone').value;
            const institution = document.getElementById('institution').value;
            const areaCity = document.getElementById('areaCity').value;
            const nativePlace = document.getElementById('nativePlace').value;
            const secretKey = document.getElementById('secretKey').value;
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirmPassword').value;
            
            const errorMsg = document.getElementById('error-msg');
            const submitBtn = document.getElementById('submit-btn');

            // VULN-018: Enforce password strength before submission
            try { validatePasswordStrength(password); } catch (strengthErr) {
                errorMsg.textContent = strengthErr.message;
                errorMsg.style.display = 'block';
                return;
            }
            if (password !== confirmPassword) {
                errorMsg.textContent = "Passwords do not match!";
                errorMsg.style.display = 'block';
                return;
            }

            submitBtn.textContent = 'Creating account...';
            submitBtn.disabled = true;
            errorMsg.style.display = 'none';

            try {
                // VULN-002 FIX: Validate role against strict allowlist — prevents privilege escalation
                const urlParams = new URLSearchParams(window.location.search);
                const rawRole = urlParams.get('role');
                const selectedRole = ALLOWED_SIGNUP_ROLES.includes(rawRole) ? rawRole : 'attendee';
                // Note: 'volunteer' role is NEVER self-assignable via signup

                const { data: authData, error: authError } = await supabase.auth.signUp({
                    email: email,
                    password: password,
                });

                if (authError) throw authError;

                if (authData && authData.user) {
                    const user = authData.user;
                    
                    // VULN-003 FIX: Validate lengths before inserting to DB
                    const { error: profileError } = await supabase.from('profiles').insert([
                        { 
                            id: user.id, 
                            role: selectedRole,  // VULN-002: validated against allowlist above
                            full_name: validateLength(fullName, 'fullName'),
                            phone_number: phone,
                            institution: validateLength(institution, 'institution'),
                            area_city: validateLength(areaCity, 'areaCity'),
                            native_place: validateLength(nativePlace, 'nativePlace'),
                            secret_key: secretKey  // Note: hashing recommended (VULN-010)
                        }
                    ]);

                    if (profileError) {
                        console.error("Profile error:", profileError);
                        // Optional: we could delete the auth user here if profile insert fails
                    }
                    
                    alert(`Account created successfully! Welcome as a new ${selectedRole}.`);
                    window.location.href = 'login.html';
                }
                
            } catch (err) {
                errorMsg.textContent = err.message;
                errorMsg.style.display = 'block';
            } finally {
                submitBtn.textContent = 'Create account';
                submitBtn.disabled = false;
            }
        });
    }
});
