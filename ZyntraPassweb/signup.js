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

            if (password !== confirmPassword) {
                errorMsg.textContent = "Passwords do not match!";
                errorMsg.style.display = 'block';
                return;
            }

            submitBtn.textContent = 'Creating account...';
            submitBtn.disabled = true;
            errorMsg.style.display = 'none';

            try {
                // Get role from URL query param, default to attendee if not specified
                const urlParams = new URLSearchParams(window.location.search);
                const selectedRole = urlParams.get('role') || 'attendee';

                const { data: authData, error: authError } = await supabase.auth.signUp({
                    email: email,
                    password: password,
                });

                if (authError) throw authError;

                if (authData && authData.user) {
                    const user = authData.user;
                    
                    const { error: profileError } = await supabase.from('profiles').insert([
                        { 
                            id: user.id, 
                            role: selectedRole, 
                            full_name: fullName,
                            phone_number: phone,
                            institution: institution,
                            area_city: areaCity,
                            native_place: nativePlace,
                            secret_key: secretKey
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
