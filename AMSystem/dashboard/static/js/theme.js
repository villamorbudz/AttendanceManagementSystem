// Theme management
function initializeTheme() {
    // Check for saved theme preference or system preference
    if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.documentElement.classList.add('dark');
        updateThemeIcons(true);
    } else {
        document.documentElement.classList.remove('dark');
        updateThemeIcons(false);
    }
}

function updateThemeIcons(isDark) {
    const sunIcons = document.querySelectorAll('.sun-icon');
    const moonIcons = document.querySelectorAll('.moon-icon');
    
    sunIcons.forEach(icon => icon.classList.toggle('hidden', isDark));
    moonIcons.forEach(icon => icon.classList.toggle('hidden', !isDark));
}

function toggleTheme() {
    const isDark = document.documentElement.classList.toggle('dark');
    localStorage.theme = isDark ? 'dark' : 'light';
    updateThemeIcons(isDark);
}

// Initialize theme on page load
document.addEventListener('DOMContentLoaded', () => {
    initializeTheme();
    
    // Add click event listeners to all theme toggle buttons
    const themeToggles = document.querySelectorAll('[data-theme-toggle]');
    themeToggles.forEach(button => {
        button.addEventListener('click', toggleTheme);
    });
});
