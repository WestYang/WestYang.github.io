document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener('click', (event) => {
        const selector = anchor.getAttribute('href');
        const target = selector ? document.querySelector(selector) : null;

        if (!target) {
            return;
        }

        event.preventDefault();
        target.scrollIntoView({ behavior: 'smooth' });
    });
});

function normalizePathname(pathname) {
    if (!pathname || pathname === '/') {
        return '/index.html';
    }

    return pathname.endsWith('/') ? `${pathname}index.html` : pathname;
}

function highlightNav() {
    const currentPath = normalizePathname(window.location.pathname);
    const navLinks = document.querySelectorAll('nav a');

    navLinks.forEach((link) => {
        const linkPath = normalizePathname(new URL(link.href).pathname);
        const isActive = currentPath === linkPath;

        link.classList.toggle('active', isActive);

        if (isActive) {
            link.setAttribute('aria-current', 'page');
        } else {
            link.removeAttribute('aria-current');
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    highlightNav();
});
