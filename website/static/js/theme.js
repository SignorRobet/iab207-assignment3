/* 
Document:   theme.js
Author:     
Date:       

This JS file is used for custom theming not achieved by Bootstrap or Flask
*/

const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');

const tooltipList = [...tooltipTriggerList].map(
    tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl)
);