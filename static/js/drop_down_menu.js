document.addEventListener('DOMContentLoaded', () => {
    const dropdownToggles = document.querySelectorAll('.sidebar .dropdown-toggle');

    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', (event) => {
            event.stopPropagation(); // Zabráníme propagaci kliknutí na rodičovské prvky
            toggle.classList.toggle('active');
            const dropdownContainer = toggle.parentElement.nextElementSibling;
            if (dropdownContainer) {
                if (dropdownContainer.style.display === 'block') {
                    dropdownContainer.style.display = 'none';
                } else {
                    dropdownContainer.style.display = 'block';
                }
            }
        });
    });
});