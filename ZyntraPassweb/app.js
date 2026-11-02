document.addEventListener('DOMContentLoaded', () => {
    const createAccountBtn = document.getElementById('create-account-btn');
    const signInBtn = document.getElementById('sign-in-btn');
    
    const roleModal = document.getElementById('role-modal');
    const closeModalBtn = document.getElementById('close-modal-btn');
    const roleButtons = document.querySelectorAll('.role-btn');

    const exploreBtn = document.querySelector(".btn-primary");
    const organizeBtn = document.querySelector(".btn-secondary");
    
    if (exploreBtn && exploreBtn.textContent.includes("Explore Events")) {
        exploreBtn.addEventListener("click", () => {
            window.location.href = "login.html";
        });
    }
    if (organizeBtn && organizeBtn.textContent.includes("Organize an Event")) {
        organizeBtn.addEventListener("click", () => {
            window.location.href = "login.html";
        });
    }

    // Sign in goes straight to login.html
    if (signInBtn) {
        signInBtn.addEventListener('click', () => {
            window.location.href = 'login.html';
        });
    }

    // Create Account shows the modal
    if (createAccountBtn) {
        createAccountBtn.addEventListener('click', () => {
            roleModal.classList.add('active');
        });
    }

    // Hide modal on Cancel
    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', () => {
            roleModal.classList.remove('active');
        });
    }

    // Handle role selection in modal -> goes to signup
    if (roleButtons) {
        roleButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const selectedRole = e.target.getAttribute('data-role');
                if (selectedRole === 'organizer') {
                    window.location.href = 'signup.html';
                } else if (selectedRole === 'attendee') {
                    window.location.href = 'attendee_signup.html';
                } else {
                    alert(`Signup for ${selectedRole.toUpperCase()} coming soon! We are building Organizer first.`);
                    roleModal.classList.remove('active');
                }
            });
        });
    }

    // Close modal if clicked outside
    if (roleModal) {
        roleModal.addEventListener('click', (e) => {
            if (e.target === roleModal) {
                roleModal.classList.remove('active');
            }
        });
    }
});
