// Main Application JavaScript

// Theme Toggle
function initTheme() {
    const toggle = document.getElementById('theme-toggle');
    const currentTheme = localStorage.getItem('theme') || 'light';

    document.documentElement.setAttribute('data-theme', currentTheme);
    updateThemeIcon(currentTheme);

    toggle.addEventListener('click', () => {
        const theme = document.documentElement.getAttribute('data-theme');
        const newTheme = theme === 'light' ? 'dark' : 'light';

        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(newTheme);
    });
}

function updateThemeIcon(theme) {
    const toggle = document.getElementById('theme-toggle');
    toggle.textContent = theme === 'light' ? '🌙' : '☀️';
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initTheme();
});
