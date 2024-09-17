/* global flatpickr */

document.addEventListener("DOMContentLoaded", function() {
    flatpickr("#specific_dates_picker", {
        mode: "multiple",
        dateFormat: "Y-m-d",
        allowInput: true,
    });
});
