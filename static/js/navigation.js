// Hamburger Menu Navigation System
// Professional navigation with collapsible sidebar

class NavigationManager {
    constructor() {
        this.sidebar = null;
        this.hamburgerBtn = null;
        this.overlay = null;
        this.isOpen = false;
        this.init();
    }

    init() {
        this.createNavigationStructure();
        this.attachEventListeners();
        this.handleResponsive();
    }

    createNavigationStructure() {
        // Create hamburger button
        this.createHamburgerButton();
        
        // Create sidebar
        this.createSidebar();
        
        // Create overlay
        this.createOverlay();
        
        // Add to page
        document.body.appendChild(this.hamburgerBtn);
        document.body.appendChild(this.sidebar);
        document.body.appendChild(this.overlay);
    }

    createHamburgerButton() {
        this.hamburgerBtn = document.createElement('button');
        this.hamburgerBtn.className = 'hamburger-btn';
        this.hamburgerBtn.innerHTML = `
            <span class="hamburger-line"></span>
            <span class="hamburger-line"></span>
            <span class="hamburger-line"></span>
        `;
        this.hamburgerBtn.setAttribute('aria-label', 'Toggle Navigation Menu');
    }

    createSidebar() {
        this.sidebar = document.createElement('nav');
        this.sidebar.className = 'sidebar-nav';
        this.sidebar.innerHTML = `
            <div class="sidebar-header">
                <div class="sidebar-logo">
                    <i class="fas fa-fingerprint"></i>
                    <span>Crime Detection</span>
                </div>
                <button class="sidebar-close" aria-label="Close Navigation">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            
            <div class="sidebar-content">
                <div class="nav-section">
                    <ul class="nav-menu">
                        <li><a href="/register" class="nav-link"><i class="fas fa-user-plus"></i> Register Suspect</a></li>
                        <li><a href="/view_criminals" class="nav-link"><i class="fas fa-users"></i> View Suspects</a></li>
                        <li><a href="/match" class="nav-link"><i class="fas fa-camera"></i> Match Face</a></li>
                        <li><a href="/match_fingerprint/live" class="nav-link"><i class="fas fa-fingerprint"></i> Match Fingerprint</a></li>
                        <li><a href="/profile" class="nav-link"><i class="fas fa-user-circle"></i> Profile</a></li>
                        <li><a href="/reports" class="nav-link"><i class="fas fa-chart-bar"></i> Reports</a></li>
                    </ul>
                </div>
                
                <div class="nav-section admin-section" id="adminSection" style="display: none;">
                    <h3 class="nav-section-title">Administration</h3>
                    <ul class="nav-menu">
                        <li><a href="/admin/manage" class="nav-link"><i class="fas fa-users-cog"></i> Manage Administrators</a></li>
                    </ul>
                </div>
                
                <div class="nav-section">
                    <ul class="nav-menu">
                        <li><a href="/logout" class="nav-link logout-link"><i class="fas fa-sign-out-alt"></i> Logout</a></li>
                    </ul>
                </div>
            </div>
            
            <div class="sidebar-footer">
                <div class="user-info">
                    <div class="user-avatar">
                        <i class="fas fa-user"></i>
                    </div>
                    <div class="user-details">
                        <span class="user-name">Admin User</span>
                        <span class="user-role">System Administrator</span>
                    </div>
                </div>
            </div>
        `;
    }

    createOverlay() {
        this.overlay = document.createElement('div');
        this.overlay.className = 'sidebar-overlay';
    }

    attachEventListeners() {
        // Hamburger button click
        this.hamburgerBtn.addEventListener('click', () => this.toggleSidebar());
        
        // Close button click
        const closeBtn = this.sidebar.querySelector('.sidebar-close');
        closeBtn.addEventListener('click', () => this.closeSidebar());
        
        // Overlay click
        this.overlay.addEventListener('click', () => this.closeSidebar());
        
        // Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen) {
                this.closeSidebar();
            }
        });
        
        // Handle nav link clicks
        const navLinks = this.sidebar.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                // Close sidebar on mobile after navigation
                if (window.innerWidth <= 768) {
                    this.closeSidebar();
                }
            });
        });
    }

    toggleSidebar() {
        if (this.isOpen) {
            this.closeSidebar();
        } else {
            this.openSidebar();
        }
    }

    openSidebar() {
        this.isOpen = true;
        this.sidebar.classList.add('open');
        this.overlay.classList.add('active');
        this.hamburgerBtn.classList.add('active');
        document.body.classList.add('sidebar-open');
        
        // Focus management for accessibility
        this.sidebar.querySelector('.sidebar-close').focus();
    }

    closeSidebar() {
        this.isOpen = false;
        this.sidebar.classList.remove('open');
        this.overlay.classList.remove('active');
        this.hamburgerBtn.classList.remove('active');
        document.body.classList.remove('sidebar-open');
        
        // Return focus to hamburger button
        this.hamburgerBtn.focus();
    }

    handleResponsive() {
        window.addEventListener('resize', () => {
            if (window.innerWidth > 768 && this.isOpen) {
                this.closeSidebar();
            }
        });
    }

    // Update user info dynamically
    updateUserInfo(name, role) {
        const userName = this.sidebar.querySelector('.user-name');
        const userRole = this.sidebar.querySelector('.user-role');
        
        if (userName) userName.textContent = name;
        if (userRole) userRole.textContent = role;
        
        // Show/hide admin section based on role
        this.updateAdminSection(role);
    }
    
    // Show/hide admin section based on user role
    updateAdminSection(role) {
        const adminSection = this.sidebar.querySelector('#adminSection');
        if (adminSection) {
            if (role === 'superadmin') {
                adminSection.style.display = 'block';
            } else {
                adminSection.style.display = 'none';
            }
        }
    }

    // Highlight current page
    setActivePage(path) {
        const navLinks = this.sidebar.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === path) {
                link.classList.add('active');
            }
        });
    }
}

// System info modal
function showSystemInfo() {
    const modal = document.createElement('div');
    modal.className = 'system-info-modal';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h3><i class="fas fa-info-circle"></i> System Information</h3>
                <button class="modal-close" onclick="this.closest('.system-info-modal').remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="modal-body">
                <div class="info-grid">
                    <div class="info-item">
                        <label>System Version:</label>
                        <span>Biometric Crime Detection v2.0</span>
                    </div>
                    <div class="info-item">
                        <label>Database:</label>
                        <span>MySQL (Production Ready)</span>
                    </div>
                    <div class="info-item">
                        <label>Scanner Mode:</label>
                        <span>Simulation + Hardware Ready</span>
                    </div>
                    <div class="info-item">
                        <label>Security Level:</label>
                        <span>Enterprise Grade</span>
                    </div>
                    <div class="info-item">
                        <label>Last Updated:</label>
                        <span>${new Date().toLocaleDateString()}</span>
                    </div>
                </div>
            </div>
        </div>
        <div class="modal-overlay" onclick="this.closest('.system-info-modal').remove()"></div>
    `;
    document.body.appendChild(modal);
}

// Initialize navigation when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const navigation = new NavigationManager();
    
    // Set active page based on current URL
    navigation.setActivePage(window.location.pathname);
    
    // Update user info if available
    const userInfo = document.querySelector('[data-user-info]');
    if (userInfo) {
        const name = userInfo.dataset.userName || 'Admin User';
        const role = userInfo.dataset.userRole || 'admin';
        navigation.updateUserInfo(name, role);
    } else {
        // Check for global admin role variable (from Flask template)
        const adminRole = window.adminRole || 'admin';
        navigation.updateAdminSection(adminRole);
    }
    
    // Make navigation globally available
    window.navigationManager = navigation;
});