// Global variables
let cartCount = 3;

// DOM elements
const mobileToggle = document.getElementById('mobileToggle');
const sidebar = document.getElementById('sidebar');
const sidebarClose = document.getElementById('sidebarClose');
const overlay = document.getElementById('overlay');
const searchBtn = document.getElementById('searchBtn');
const searchInput = document.getElementById('searchInput');
const cartCountElement = document.getElementById('cartCount');

// Mobile menu functionality
function openSidebar() {
    sidebar.classList.add('active');
    overlay.style.display = 'block';
    document.body.style.overflow = 'hidden';
}
function closeSidebar() {
    sidebar.classList.remove('active');
    overlay.style.display = 'none';
    document.body.style.overflow = 'auto';
}
if (mobileToggle) mobileToggle.addEventListener('click', openSidebar);
if (sidebarClose) sidebarClose.addEventListener('click', closeSidebar);
if (overlay) overlay.addEventListener('click', closeSidebar);

// Close sidebar on escape key
document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && sidebar.classList.contains('active')) {
        closeSidebar();
    }
});

// Scroll animations
function initScrollAnimations() {
    const observerOptions = { threshold: 0.1, rootMargin: '0px 0px -50px 0px' };
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) entry.target.classList.add('visible');
        });
    }, observerOptions);
    document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));
}

// Product card hover effects
function initProductEffects() {
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-10px) scale(1.02)';
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0) scale(1)';
        });
    });
}

// Category handlers (added to fix ReferenceError)
function initCategoryHandlers() {
    const categories = document.querySelectorAll('.category-item');
    if (!categories.length) return;
    categories.forEach(cat => {
        cat.addEventListener('click', (e) => {
            e.preventDefault();
            const name = cat.dataset.name || cat.textContent.trim();
            categories.forEach(c => c.classList.remove('active'));
            cat.classList.add('active');
            console.log('Category selected:', name);
        });
    });
}

// Header scroll effect
function initHeaderEffects() {
    const header = document.querySelector('.main-nav');
    if (!header) return;
    window.addEventListener('scroll', () => {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        if (scrollTop > 100) {
            header.style.background = 'rgba(255, 255, 255, 0.95)';
            header.style.backdropFilter = 'blur(10px)';
        } else {
            header.style.background = 'white';
            header.style.backdropFilter = 'none';
        }
    });
}

// Smooth scroll to top
function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Add scroll to top button
function initScrollToTop() {
    const scrollButton = document.createElement('button');
    scrollButton.textContent = '↑';
    scrollButton.className = 'scroll-to-top';
    scrollButton.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: var(--primary-color);
        color: white;
        border: none;
        font-size: 18px;
        cursor: pointer;
        z-index: 1000;
        opacity: 0;
        transform: translateY(20px);
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0,123,255,0.3);
    `;
    scrollButton.addEventListener('click', scrollToTop);
    document.body.appendChild(scrollButton);
    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            scrollButton.style.opacity = '1';
            scrollButton.style.transform = 'translateY(0)';
        } else {
            scrollButton.style.opacity = '0';
            scrollButton.style.transform = 'translateY(20px)';
        }
    });
}

// Lazy loading for images
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                imageObserver.unobserve(img);
            }
        });
    });
    images.forEach(img => imageObserver.observe(img));
}

// Sidebar dropdown toggle
function initSidebarDropdowns() {
    document.querySelectorAll('.sidebar-dropdown > a').forEach(toggle => {
        toggle.addEventListener('click', function (e) {
            e.preventDefault();
            let submenu = this.nextElementSibling;
            submenu.style.display = submenu.style.display === 'block' ? 'none' : 'block';
        });
    });
}

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#28a745' : type === 'error' ? '#dc3545' : '#007bff'};
        color: white;
        padding: 12px 20px;
        border-radius: 6px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        opacity: 0;
        transform: translateY(-20px);
        transition: all 0.3s ease;
        z-index: 2000;
    `;
    document.body.appendChild(notification);
    requestAnimationFrame(() => {
        notification.style.opacity = '1';
        notification.style.transform = 'translateY(0)';
    });
    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transform = 'translateY(-20px)';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Run all initializers immediately
initScrollAnimations();
initProductEffects();
initCategoryHandlers();
initHeaderEffects();
initScrollToTop();
initLazyLoading();
initSidebarDropdowns();

// Handle window resize
window.addEventListener('resize', function () {
    if (window.innerWidth > 991 && sidebar.classList.contains('active')) {
        closeSidebar();
    }
});

// Keyboard navigation
document.addEventListener('keydown', function (e) {
    // Alt + S for search focus
    if (e.altKey && e.key === 's') {
        e.preventDefault();
        if (searchInput) searchInput.focus();
    }
    // Alt + C for cart
    if (e.altKey && e.key === 'c') {
        e.preventDefault();
        showNotification('Cart opened!', 'info');
    }
});
