// Modern Interactions and Animations
document.addEventListener('DOMContentLoaded', function() {
    
    // Disable form submission animation for login issues
    const loginForm = document.querySelector('form[method="post"]');
    if (loginForm && window.location.pathname.includes('login')) {
        const submitBtn = loginForm.querySelector('button[type="submit"]');
        if (submitBtn) {
            submitBtn.addEventListener('click', function(e) {
                // Don't prevent default, just disable the loading animation
                this.disabled = false;
            });
        }
    }
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add loading state to buttons (except login form)
    document.querySelectorAll('button[type="submit"], input[type="submit"]').forEach(button => {
        // Skip login form buttons to avoid login issues
        if (button.closest('form') && window.location.pathname.includes('login')) {
            return;
        }
        
        button.addEventListener('click', function() {
            const originalText = this.textContent || this.value;
            const isInput = this.tagName === 'INPUT';
            
            if (isInput) {
                this.value = 'Processing...';
            } else {
                this.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
            }
            
            this.disabled = true;
            
            // Re-enable after 3 seconds (fallback)
            setTimeout(() => {
                this.disabled = false;
                if (isInput) {
                    this.value = originalText;
                } else {
                    this.textContent = originalText;
                }
            }, 3000);
        });
    });

    // Enhanced form validation feedback
    document.querySelectorAll('.form-control').forEach(input => {
        input.addEventListener('blur', function() {
            if (this.checkValidity()) {
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
            } else {
                this.classList.remove('is-valid');
                this.classList.add('is-invalid');
            }
        });

        input.addEventListener('input', function() {
            this.classList.remove('is-invalid', 'is-valid');
        });
    });

    // Animate numbers in statistics section
    function animateNumbers() {
        const numbers = document.querySelectorAll('.number[data-number]');
        
        numbers.forEach(number => {
            const target = parseInt(number.getAttribute('data-number'));
            const duration = 2000;
            const step = target / (duration / 16);
            let current = 0;
            
            const timer = setInterval(() => {
                current += step;
                if (current >= target) {
                    current = target;
                    clearInterval(timer);
                }
                number.textContent = Math.floor(current).toLocaleString();
            }, 16);
        });
    }

    // Trigger number animation when section is visible
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateNumbers();
                observer.unobserve(entry.target);
            }
        });
    });

    const statsSection = document.querySelector('.section-counter');
    if (statsSection) {
        observer.observe(statsSection);
    }

    // Add fade-in animation to elements
    const fadeElements = document.querySelectorAll('.fade-in-up');
    const fadeObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    });

    fadeElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        fadeObserver.observe(el);
    });

    // Enhanced search functionality
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput) {
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.toLowerCase();
            
            if (query.length > 0) {
                this.classList.add('searching');
                
                searchTimeout = setTimeout(() => {
                    this.classList.remove('searching');
                }, 500);
            }
        });
    }

    // Toast notifications for form submissions
    function showToast(message, type = 'success') {
        const toast = document.createElement('div');
        toast.className = `toast-notification toast-${type}`;
        toast.innerHTML = `
            <div class="toast-content">
                <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'} me-2"></i>
                ${message}
            </div>
        `;
        
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.classList.add('show');
        }, 100);
        
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => {
                document.body.removeChild(toast);
            }, 300);
        }, 3000);
    }

    // Add CSS for toast notifications
    const toastStyles = `
        .toast-notification {
            position: fixed;
            top: 20px;
            right: 20px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            padding: 16px 20px;
            z-index: 9999;
            transform: translateX(100%);
            transition: transform 0.3s ease;
            border-left: 4px solid var(--success);
        }
        
        .toast-notification.toast-error {
            border-left-color: var(--danger);
        }
        
        .toast-notification.show {
            transform: translateX(0);
        }
        
        .toast-content {
            display: flex;
            align-items: center;
            font-weight: 500;
            color: var(--gray-700);
        }
        
        .searching {
            background-image: linear-gradient(90deg, transparent, rgba(37, 99, 235, 0.1), transparent);
            background-size: 200% 100%;
            animation: searchPulse 1s infinite;
        }
        
        @keyframes searchPulse {
            0% { background-position: -200% 0; }
            100% { background-position: 200% 0; }
        }
    `;
    
    const styleSheet = document.createElement('style');
    styleSheet.textContent = toastStyles;
    document.head.appendChild(styleSheet);

    // Enhanced card hover effects
    document.querySelectorAll('.job-card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-4px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Parallax effect for hero sections
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const parallax = document.querySelector('.hero');
        
        if (parallax) {
            const speed = scrolled * 0.5;
            parallax.style.transform = `translateY(${speed}px)`;
        }
    });

    // Auto-hide alerts after 5 seconds
    document.querySelectorAll('.alert').forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-20px)';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 5000);
    });
});

// Utility function for smooth page transitions
function smoothPageTransition(url) {
    document.body.style.opacity = '0.8';
    document.body.style.transform = 'scale(0.98)';
    
    setTimeout(() => {
        window.location.href = url;
    }, 200);
}

// Add to all internal links
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('a[href^="/"], a[href^="' + window.location.origin + '"]').forEach(link => {
        link.addEventListener('click', function(e) {
            if (!this.target || this.target === '_self') {
                e.preventDefault();
                smoothPageTransition(this.href);
            }
        });
    });
});