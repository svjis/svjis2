"use strict";

const imageDialog = document.querySelector('#advert-image-dialog');

if (imageDialog && typeof imageDialog.showModal === 'function') {
    const dialogImage = imageDialog.querySelector('.advert-image-dialog-image');

    document.querySelectorAll('.advert-image-preview-link').forEach(function (previewLink) {
        previewLink.addEventListener('click', function (event) {
            const previewImage = previewLink.querySelector('.advert-image-preview');

            event.preventDefault();
            dialogImage.src = previewLink.href;
            dialogImage.alt = previewImage.alt;
            imageDialog.showModal();
        });
    });

    imageDialog.addEventListener('click', function (event) {
        if (event.target === imageDialog || event.target.classList.contains('advert-image-dialog-close')) {
            imageDialog.close();
        }
    });
}
