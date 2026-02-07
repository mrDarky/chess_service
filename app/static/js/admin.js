// Admin panel JavaScript

const token = localStorage.getItem('token');
const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
};

// Check admin access
async function checkAdminAccess() {
    if (!token) {
        window.location.href = '/login';
        return;
    }
    
    try {
        const response = await fetch('/auth/me', { headers });
        if (response.ok) {
            const user = await response.json();
            if (!user.is_admin) {
                alert('Access denied. Admin privileges required.');
                window.location.href = '/dashboard';
            }
        } else {
            window.location.href = '/login';
        }
    } catch (error) {
        window.location.href = '/login';
    }
}

// Load statistics
async function loadStats() {
    try {
        const response = await fetch('/admin/stats', { headers });
        if (response.ok) {
            const stats = await response.json();
            document.getElementById('totalUsers').textContent = stats.users;
            document.getElementById('totalCourses').textContent = stats.courses;
            document.getElementById('totalPuzzles').textContent = stats.puzzles;
            document.getElementById('totalRevenue').textContent = '$' + (stats.revenue || 0).toFixed(2);
        }
    } catch (error) {
        console.error('Failed to load stats');
    }
}

// Users management
async function loadUsers() {
    try {
        const response = await fetch('/admin/users', { headers });
        if (response.ok) {
            const users = await response.json();
            const container = document.getElementById('usersList');
            
            container.innerHTML = `
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Username</th>
                                <th>Email</th>
                                <th>Rating</th>
                                <th>Admin</th>
                                <th>Created</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${users.map(user => `
                                <tr>
                                    <td>${user.id}</td>
                                    <td>${user.username}</td>
                                    <td>${user.email}</td>
                                    <td>${user.rating}</td>
                                    <td>${user.is_admin ? '✓' : ''}</td>
                                    <td>${new Date(user.created_at).toLocaleDateString()}</td>
                                    <td>
                                        <button class="btn btn-sm btn-warning" onclick="toggleAdmin(${user.id}, ${!user.is_admin})">
                                            ${user.is_admin ? 'Remove Admin' : 'Make Admin'}
                                        </button>
                                        <button class="btn btn-sm btn-danger" onclick="deleteUser(${user.id})">Delete</button>
                                    </td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            `;
        }
    } catch (error) {
        console.error('Failed to load users');
    }
}

async function toggleAdmin(userId, isAdmin) {
    try {
        const response = await fetch(`/admin/users/${userId}/admin?is_admin=${isAdmin}`, {
            method: 'PUT',
            headers
        });
        if (response.ok) {
            showAlert('User updated successfully', 'success');
            loadUsers();
        }
    } catch (error) {
        showAlert('Failed to update user', 'danger');
    }
}

async function deleteUser(userId) {
    if (!confirm('Are you sure you want to delete this user?')) return;
    
    try {
        const response = await fetch(`/admin/users/${userId}`, {
            method: 'DELETE',
            headers
        });
        if (response.ok) {
            showAlert('User deleted successfully', 'success');
            loadUsers();
        }
    } catch (error) {
        showAlert('Failed to delete user', 'danger');
    }
}

// Categories management
async function loadCategories() {
    try {
        const response = await fetch('/categories/');
        if (response.ok) {
            const categories = await response.json();
            
            // Update category lists in forms
            updateCategorySelects(categories);
            
            // Display categories
            const container = document.getElementById('categoriesList');
            container.innerHTML = `
                <div class="list-group">
                    ${categories.map(cat => `
                        <div class="list-group-item d-flex justify-content-between align-items-center">
                            <div>
                                <h6 class="mb-1">${cat.name}</h6>
                                <small class="text-muted">${cat.description || 'No description'}</small>
                            </div>
                            <div>
                                <button class="btn btn-sm btn-primary" onclick="editCategory(${cat.id})">Edit</button>
                                <button class="btn btn-sm btn-danger" onclick="deleteCategory(${cat.id})">Delete</button>
                            </div>
                        </div>
                    `).join('')}
                </div>
            `;
        }
    } catch (error) {
        console.error('Failed to load categories');
    }
}

function updateCategorySelects(categories) {
    const selects = [
        document.getElementById('courseCategoryId'),
        document.getElementById('puzzleCategoryId')
    ];
    
    selects.forEach(select => {
        if (select) {
            const currentValue = select.value;
            select.innerHTML = '<option value="">None</option>' +
                categories.map(cat => `<option value="${cat.id}">${cat.name}</option>`).join('');
            select.value = currentValue;
        }
    });
}

function showCategoryForm() {
    document.getElementById('categoryForm').style.display = 'block';
    document.getElementById('categoryId').value = '';
    document.getElementById('categoryName').value = '';
    document.getElementById('categoryDescription').value = '';
}

function hideCategoryForm() {
    document.getElementById('categoryForm').style.display = 'none';
}

async function saveCategory() {
    const id = document.getElementById('categoryId').value;
    const data = {
        name: document.getElementById('categoryName').value,
        description: document.getElementById('categoryDescription').value
    };
    
    try {
        const url = id ? `/categories/${id}` : '/categories/';
        const method = id ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method,
            headers,
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            showAlert('Category saved successfully', 'success');
            hideCategoryForm();
            loadCategories();
        }
    } catch (error) {
        showAlert('Failed to save category', 'danger');
    }
}

async function editCategory(id) {
    try {
        const response = await fetch(`/categories/${id}`);
        if (response.ok) {
            const category = await response.json();
            document.getElementById('categoryId').value = category.id;
            document.getElementById('categoryName').value = category.name;
            document.getElementById('categoryDescription').value = category.description || '';
            showCategoryForm();
        }
    } catch (error) {
        console.error('Failed to load category');
    }
}

async function deleteCategory(id) {
    if (!confirm('Are you sure you want to delete this category?')) return;
    
    try {
        const response = await fetch(`/categories/${id}`, {
            method: 'DELETE',
            headers
        });
        if (response.ok) {
            showAlert('Category deleted successfully', 'success');
            loadCategories();
        }
    } catch (error) {
        showAlert('Failed to delete category', 'danger');
    }
}

// Courses management
async function loadCourses() {
    try {
        const response = await fetch('/courses/');
        if (response.ok) {
            const courses = await response.json();
            const container = document.getElementById('coursesList');
            
            container.innerHTML = `
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Title</th>
                                <th>Price</th>
                                <th>Difficulty</th>
                                <th>Category</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${courses.map(course => `
                                <tr>
                                    <td>${course.title}</td>
                                    <td>$${course.price.toFixed(2)}</td>
                                    <td><span class="badge bg-info">${course.difficulty}</span></td>
                                    <td>${course.category_name || '-'}</td>
                                    <td>
                                        <button class="btn btn-sm btn-primary" onclick="editCourse(${course.id})">Edit</button>
                                        <button class="btn btn-sm btn-danger" onclick="deleteCourse(${course.id})">Delete</button>
                                    </td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            `;
        }
    } catch (error) {
        console.error('Failed to load courses');
    }
}

function showCourseForm() {
    document.getElementById('courseForm').style.display = 'block';
    document.getElementById('courseId').value = '';
    document.getElementById('courseTitle').value = '';
    document.getElementById('courseDescription').value = '';
    document.getElementById('coursePrice').value = '';
    document.getElementById('courseCategoryId').value = '';
    document.getElementById('courseDifficulty').value = 'beginner';
}

function hideCourseForm() {
    document.getElementById('courseForm').style.display = 'none';
}

async function saveCourse() {
    const id = document.getElementById('courseId').value;
    const data = {
        title: document.getElementById('courseTitle').value,
        description: document.getElementById('courseDescription').value,
        price: parseFloat(document.getElementById('coursePrice').value),
        category_id: document.getElementById('courseCategoryId').value || null,
        difficulty: document.getElementById('courseDifficulty').value
    };
    
    try {
        const url = id ? `/courses/${id}` : '/courses/';
        const method = id ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method,
            headers,
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            showAlert('Course saved successfully', 'success');
            hideCourseForm();
            loadCourses();
        }
    } catch (error) {
        showAlert('Failed to save course', 'danger');
    }
}

async function editCourse(id) {
    try {
        const response = await fetch(`/courses/${id}`);
        if (response.ok) {
            const course = await response.json();
            document.getElementById('courseId').value = course.id;
            document.getElementById('courseTitle').value = course.title;
            document.getElementById('courseDescription').value = course.description || '';
            document.getElementById('coursePrice').value = course.price;
            document.getElementById('courseCategoryId').value = course.category_id || '';
            document.getElementById('courseDifficulty').value = course.difficulty;
            showCourseForm();
        }
    } catch (error) {
        console.error('Failed to load course');
    }
}

async function deleteCourse(id) {
    if (!confirm('Are you sure you want to delete this course?')) return;
    
    try {
        const response = await fetch(`/courses/${id}`, {
            method: 'DELETE',
            headers
        });
        if (response.ok) {
            showAlert('Course deleted successfully', 'success');
            loadCourses();
        }
    } catch (error) {
        showAlert('Failed to delete course', 'danger');
    }
}

// Puzzles management
async function loadPuzzles() {
    try {
        const response = await fetch('/puzzles/');
        if (response.ok) {
            const puzzles = await response.json();
            const container = document.getElementById('puzzlesList');
            
            container.innerHTML = `
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Title</th>
                                <th>Difficulty</th>
                                <th>Rating</th>
                                <th>Solution</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${puzzles.map(puzzle => `
                                <tr>
                                    <td>${puzzle.title}</td>
                                    <td><span class="badge bg-${puzzle.difficulty === 'easy' ? 'success' : puzzle.difficulty === 'medium' ? 'warning' : 'danger'}">${puzzle.difficulty}</span></td>
                                    <td>${puzzle.rating}</td>
                                    <td><code>${puzzle.solution}</code></td>
                                    <td>
                                        <button class="btn btn-sm btn-primary" onclick="editPuzzle(${puzzle.id})">Edit</button>
                                        <button class="btn btn-sm btn-danger" onclick="deletePuzzle(${puzzle.id})">Delete</button>
                                    </td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            `;
        }
    } catch (error) {
        console.error('Failed to load puzzles');
    }
}

function showPuzzleForm() {
    document.getElementById('puzzleForm').style.display = 'block';
    document.getElementById('puzzleId').value = '';
    document.getElementById('puzzleTitle').value = '';
    document.getElementById('puzzleFen').value = '';
    document.getElementById('puzzleSolution').value = '';
    document.getElementById('puzzleDifficulty').value = 'easy';
    document.getElementById('puzzleRating').value = '1200';
    document.getElementById('puzzleCategoryId').value = '';
}

function hidePuzzleForm() {
    document.getElementById('puzzleForm').style.display = 'none';
}

async function savePuzzle() {
    const id = document.getElementById('puzzleId').value;
    const data = {
        title: document.getElementById('puzzleTitle').value,
        fen: document.getElementById('puzzleFen').value,
        solution: document.getElementById('puzzleSolution').value,
        difficulty: document.getElementById('puzzleDifficulty').value,
        rating: parseInt(document.getElementById('puzzleRating').value),
        category_id: document.getElementById('puzzleCategoryId').value || null
    };
    
    try {
        const url = id ? `/puzzles/${id}` : '/puzzles/';
        const method = id ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method,
            headers,
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            showAlert('Puzzle saved successfully', 'success');
            hidePuzzleForm();
            loadPuzzles();
        }
    } catch (error) {
        showAlert('Failed to save puzzle', 'danger');
    }
}

async function editPuzzle(id) {
    try {
        const response = await fetch(`/puzzles/${id}`);
        if (response.ok) {
            const puzzle = await response.json();
            document.getElementById('puzzleId').value = puzzle.id;
            document.getElementById('puzzleTitle').value = puzzle.title;
            document.getElementById('puzzleFen').value = puzzle.fen;
            document.getElementById('puzzleSolution').value = puzzle.solution;
            document.getElementById('puzzleDifficulty').value = puzzle.difficulty;
            document.getElementById('puzzleRating').value = puzzle.rating;
            document.getElementById('puzzleCategoryId').value = puzzle.category_id || '';
            showPuzzleForm();
        }
    } catch (error) {
        console.error('Failed to load puzzle');
    }
}

async function deletePuzzle(id) {
    if (!confirm('Are you sure you want to delete this puzzle?')) return;
    
    try {
        const response = await fetch(`/puzzles/${id}`, {
            method: 'DELETE',
            headers
        });
        if (response.ok) {
            showAlert('Puzzle deleted successfully', 'success');
            loadPuzzles();
        }
    } catch (error) {
        showAlert('Failed to delete puzzle', 'danger');
    }
}

// Utility functions
function showAlert(message, type) {
    const container = document.getElementById('alertContainer');
    container.innerHTML = `<div class="alert alert-${type} alert-dismissible fade show" role="alert">
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    </div>`;
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    checkAdminAccess();
    loadStats();
    loadUsers();
    loadCategories();
    loadCourses();
    loadPuzzles();
    
    // Tab change event listener
    document.querySelectorAll('button[data-bs-toggle="tab"]').forEach(tab => {
        tab.addEventListener('shown.bs.tab', function (event) {
            const targetId = event.target.getAttribute('data-bs-target').substring(1);
            if (targetId === 'users') loadUsers();
            else if (targetId === 'categories') loadCategories();
            else if (targetId === 'courses') loadCourses();
            else if (targetId === 'puzzles') loadPuzzles();
        });
    });
});
