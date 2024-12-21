'use strict';

document.addEventListener('DOMContentLoaded', function () {
    /* ===============================================================
		GLIGHTBOX
	=============================================================== */
    const lightbox = GLightbox({
        touchNavigation: true,
    });

    /* ===============================================================
		NAVBAR TOGGLING
	=============================================================== */
    document.querySelector('.navbar-toggler').addEventListener('click', function () {
        document.querySelector('.navbar-toggler').classList.toggle('active');
    });
});
