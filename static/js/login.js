/**
 * Biometric Crime Detection System
 * Login Page JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    // Password visibility toggle
    const togglePassword = document.getElementById('togglePassword');
    const password = document.getElementById('password');
    
    if (togglePassword && password) {
        togglePassword.addEventListener('click', function() {
            const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
            password.setAttribute('type', type);
            this.classList.toggle('fa-eye');
            this.classList.toggle('fa-eye-slash');
        });
    }
    
    // Form submission animation (Flask handles the actual submission)
    const loginForm = document.getElementById('login-form');
    const loginBtn = document.querySelector('.login-btn');
    
    if (loginForm && loginBtn) {
        loginForm.addEventListener('submit', function(e) {
            // Don't prevent default - let Flask handle the form submission
            loginBtn.classList.add('loading');
            loginBtn.innerHTML = '<span>Authenticating</span><div class="spinner"></div>';
            
            // Form will submit normally to Flask backend
         });
    }
    
    // Background animation with cyber particles
    initCyberParticles();
});

/**
 * Initialize cyber particles animation in the background
 */
function initCyberParticles() {
    const loginContainer = document.querySelector('.login-container');
    let particles = [];
    
    if (!loginContainer) return;
    
    // Create a particle
    function createParticle() {
        const particle = document.createElement('div');
        particle.classList.add('cyber-particle');
        
        // Random position
        const posX = Math.random() * 100;
        const posY = Math.random() * 100;
        
        // Random size
        const size = Math.random() * 5 + 1;
        
        // Random opacity and color variation
        const opacity = Math.random() * 0.5 + 0.2;
        const hue = 190 + Math.random() * 20; // Blue-cyan color range
        
        // Apply styles
        particle.style.left = posX + '%';
        particle.style.top = posY + '%';
        particle.style.width = size + 'px';
        particle.style.height = size + 'px';
        particle.style.opacity = opacity;
        particle.style.backgroundColor = `hsla(${hue}, 100%, 60%, ${opacity})`;
        
        loginContainer.appendChild(particle);
        particles.push(particle);
        
        // Remove particles after animation completes
        setTimeout(() => {
            particle.remove();
            particles = particles.filter(p => p !== particle);
        }, 5000);
    }
    
    // Create particles periodically
    setInterval(createParticle, 300);
    
    // Create initial batch of particles
    for (let i = 0; i < 10; i++) {
        setTimeout(() => createParticle(), i * 200);
    }
    
    // Add subtle matrix-like digital rain effect
    createDigitalRain();
}

/**
 * Create a subtle digital rain effect in the background
 */
function createDigitalRain() {
    const loginContainer = document.querySelector('.login-container');
    if (!loginContainer) return;
    
    const canvas = document.createElement('canvas');
    canvas.classList.add('digital-rain');
    canvas.style.position = 'absolute';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100%';
    canvas.style.height = '100%';
    canvas.style.zIndex = '0';
    canvas.style.opacity = '0.15';
    loginContainer.appendChild(canvas);
    
    const ctx = canvas.getContext('2d');
    
    // Set canvas dimensions
    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
    
    // Characters for the digital rain
    const chars = '01'.split('');
    const columns = Math.floor(canvas.width / 20);
    const drops = [];
    
    // Initialize drops
    for (let i = 0; i < columns; i++) {
        drops[i] = Math.random() * -100;
    }
    
    function draw() {
        // Semi-transparent black background to create trail effect
        ctx.fillStyle = 'rgba(10, 14, 23, 0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        ctx.fillStyle = '#4cc9f0';
        ctx.font = '15px monospace';
        
        // Draw characters
        for (let i = 0; i < drops.length; i++) {
            // Random character
            const char = chars[Math.floor(Math.random() * chars.length)];
            // x coordinate of the drop
            const x = i * 20;
            // y coordinate of the drop
            const y = drops[i] * 20;
            
            ctx.fillText(char, x, y);
            
            // Send the drop back to the top randomly after it crosses the screen
            if (y > canvas.height && Math.random() > 0.975) {
                drops[i] = 0;
            }
            
            // Move drop down
            drops[i]++;
        }
    }
    
    // Animation loop
    setInterval(draw, 50);
}