document.addEventListener('DOMContentLoaded', () => {
    const dropdownToggles = document.querySelectorAll('.sidebar .dropdown-toggle');

    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', () => {
            toggle.classList.toggle('active');
            const dropdownContainer = toggle.nextElementSibling;
            if (dropdownContainer) {
                dropdownContainer.style.display = dropdownContainer.style.display === 'block' ? 'none' : 'block';
            }
        });
    });
});