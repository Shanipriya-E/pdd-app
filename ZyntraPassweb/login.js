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

    // UI Logic for Role Selection
    const roleOptions = document.querySelectorAll('.role-option');
    const hiddenRoleInput = document.getElementById('selectedRole');
    const secretKeyGroup = document.getElementById('secretKeyGroup');
    const secretKeyInput = document.getElementById('secretKey');
    const emailGroup = document.getElementById('emailGroup');
    const passwordGroup = document.getElementById('passwordGroup');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const volunteerCodeGroup = document.getElementById('volunteerCodeGroup');
    const volunteerCodeInput = document.getElementById('volunteerCode');
    const rememberForgotGroup = document.getElementById('rememberForgotGroup');
    const createAccountLink = document.getElementById('create-account-link');

    if (roleOptions) {
        roleOptions.forEach(option => {
            option.addEventListener('click', () => {
                roleOptions.forEach(opt => opt.classList.remove('selected'));
                option.classList.add('selected');
                
                const role = option.getAttribute('data-role');
                hiddenRoleInput.value = role;

                if (role === 'organizer') {
                    secretKeyGroup.style.display = 'block';
                    secretKeyInput.required = true;
                    volunteerCodeGroup.style.display = 'none';
                    volunteerCodeInput.required = false;
                    emailGroup.style.display = 'block';
                    passwordGroup.style.display = 'block';
                    emailInput.required = true;
                    passwordInput.required = true;
                    rememberForgotGroup.style.display = 'flex';
                } else if (role === 'volunteer') {
                    secretKeyGroup.style.display = 'none';
                    secretKeyInput.required = false;
                    volunteerCodeGroup.style.display = 'block';
                    volunteerCodeInput.required = true;
                    emailGroup.style.display = 'none';
                    passwordGroup.style.display = 'none';
                    emailInput.required = false;
                    passwordInput.required = false;
                    rememberForgotGroup.style.display = 'none';
                } else {
                    secretKeyGroup.style.display = 'none';
                    secretKeyInput.required = false;
                    volunteerCodeGroup.style.display = 'none';
                    volunteerCodeInput.required = false;
                    emailGroup.style.display = 'block';
                    passwordGroup.style.display = 'block';
                    emailInput.required = true;
                    passwordInput.required = true;
                    rememberForgotGroup.style.display = 'flex';
                }
            });
        });
    }

    if (createAccountLink) {
        createAccountLink.addEventListener('click', (e) => {
            e.preventDefault();
            const role = hiddenRoleInput.value;
            if (!role) {
                alert("Please select a role (Attendee, Organizer, or Volunteer) first by clicking one of the options above!");
                return;
            }
            
            if (role === 'organizer') {
                window.location.href = 'signup.html?role=' + role;
            } else {
                
                window.location.href = 'signup.html?role=' + role;
            }
        });
    }

    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            if (!supabase) {
                alert("Database connection not ready. Try running on a local server instead of file://");
                return;
            }

            const role = hiddenRoleInput.value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const enteredSecretKey = document.getElementById('secretKey').value;
            const enteredVolunteerCode = document.getElementById('volunteerCode').value;
            
            const errorMsg = document.getElementById('error-msg');
            const submitBtn = document.getElementById('submit-btn');

            if (!role) {
                errorMsg.textContent = "Please select who you are signing in as.";
                errorMsg.style.display = 'block';
                return;
            }

            submitBtn.textContent = 'Authenticating...';
            submitBtn.disabled = true;
            errorMsg.style.display = 'none';

            try {
                if (role === 'volunteer') {
                    // Volunteer login logic based on 4-digit code
                    const { data: volData, error: volError } = await supabase
                        .from('volunteers')
                        .select('id, user_id, event_id')
                        .eq('secret_code', enteredVolunteerCode)
                        .eq('status', 'approved')
                        .maybeSingle();
                        
                    if (volError) throw volError;
                    
                    if (!volData) {
                        throw new Error("Invalid Volunteer Code! Access Denied.");
                    }
                    
                    // We successfully found the volunteer. Save in localStorage for the dashboard.
                    localStorage.setItem('volunteer_code', enteredVolunteerCode);
                    localStorage.setItem('volunteer_user_id', volData.user_id);
                    localStorage.setItem('volunteer_event_id', volData.event_id);
                    localStorage.setItem('volunteer_id', volData.id);
                    
                    alert(`Authentication Successful! Welcome Volunteer.`);
                    window.location.href = 'volunteer_dashboard.html';
                    return; // Skip normal auth
                }

                const { data: authData, error: authError } = await supabase.auth.signInWithPassword({
                    email: email,
                    password: password,
                });

                if (authError) throw authError;
                const user = authData.user;

                const { data: profileData, error: profileError } = await supabase
                    .from('profiles')
                    .select('role, secret_key')
                    .eq('id', user.id)
                    .single();

                if (profileError) throw profileError;

                if (profileData.role !== role) {
                    await supabase.auth.signOut();
                    throw new Error(`This account belongs to a ${profileData.role}, not a ${role}.`);
                }

                if (role === 'organizer' && profileData.secret_key !== enteredSecretKey) {
                    await supabase.auth.signOut();
                    throw new Error("Invalid Secret Key! Access Denied.");
                }

                alert(`Authentication Successful! Welcome back, ${role}.`);
                
                if (role === 'organizer') {
                    window.location.href = 'dashboard.html';
                } else if (role === 'attendee') {
                    window.location.href = 'attendee_dashboard.html';
                } else if (role === 'volunteer') {
                    window.location.href = 'volunteers.html';
                } else {
                    window.location.href = 'index.html';
                }
                
            } catch (err) {
                errorMsg.textContent = err.message;
                errorMsg.style.display = 'block';
            } finally {
                submitBtn.textContent = 'Login';
                submitBtn.disabled = false;
            }
        });
    }
});

