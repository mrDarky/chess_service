// Authentication helper functions

function checkAuth() {
    const token = localStorage.getItem('token');
    const loginLink = document.getElementById('loginLink');
    const registerLink = document.getElementById('registerLink');
    const userMenu = document.getElementById('userMenu');
    
    if (token) {
        // Hide login/register links
        if (loginLink) loginLink.style.display = 'none';
        if (registerLink) registerLink.style.display = 'none';
        
        // Show user menu
        if (userMenu) userMenu.classList.remove('d-none');
        
        // Fetch user info
        fetchUserInfo(token);
    } else {
        // Show login/register links
        if (loginLink) loginLink.style.display = 'block';
        if (registerLink) registerLink.style.display = 'block';
        
        // Hide user menu
        if (userMenu) userMenu.classList.add('d-none');
    }
}

async function fetchUserInfo(token) {
    try {
        const response = await fetch('/auth/me', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            const user = await response.json();
            const usernameSpan = document.getElementById('navUsername');
            if (usernameSpan) {
                usernameSpan.textContent = user.username;
            }
            
            // Show/hide admin link based on user role
            const adminLink = document.getElementById('adminLink');
            if (adminLink) {
                if (user.is_admin) {
                    adminLink.style.display = 'block';
                } else {
                    adminLink.style.display = 'none';
                }
            }
        } else if (response.status === 401) {
            // Token expired, clear it
            localStorage.removeItem('token');
            checkAuth();
        }
    } catch (error) {
        console.error('Failed to fetch user info:', error);
    }
}

function logout() {
    localStorage.removeItem('token');
    window.location.href = '/';
}

// Check auth on page load
document.addEventListener('DOMContentLoaded', checkAuth);
