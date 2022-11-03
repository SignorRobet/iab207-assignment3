/* 
Document:   theme.js
Author:     
Date:       

This JS file is used for custom theming not achieved by Bootstrap or Flask
*/

// Custom Navbar tooltips
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
const tooltipList = [...tooltipTriggerList].map(
    tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl)
);

// Input image preview Element
function PreviewImage() {
    var oFReader = new FileReader();
    const imgInput = document.getElementById("imgInput");
    const imgPreview = document.getElementById("imgPreview");

    if (!Object.is(imgInput, null) && !Object.is(imgPreview, null)) {
        oFReader.readAsDataURL(imgInput.files[0]);

        oFReader.onload = function (oFREvent) {
            imgPreview.src = oFREvent.target.result;
        };
    };
};

function calculateSubtotal(ticketQuantity, ticketPrice) {
    const quantityValue = parseInt(ticketQuantity);
    const priceValue = parseFloat(ticketPrice);

    if (!Number.isNaN(quantityValue) && !Number.isNaN(priceValue) && quantityValue >= 0) {
        return '$' + (quantityValue * priceValue).toFixed(2);
    }
    else {
        return '$' + 0 + '.00';
    }
};
