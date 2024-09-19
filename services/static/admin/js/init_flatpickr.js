/* global flatpickr */

/**
 * Initialises the Flatpickr date picker for selecting multiple specific dates.
 *
 * This script waits for the DOM to be fully loaded before activating the Flatpickr 
 * plugin on the element with the ID `#specific_dates_picker`.
 *
 * The date picker is configured with the following options:
 * - mode: "multiple" - Allows the selection of multiple dates.
 * - dateFormat: "Y-m-d" - Formats the selected dates as 'Year-Month-Day'.
 * - allowInput: true - Permits manual input of dates in addition to using the date picker.
 *
 * The script assumes that the Flatpickr library (`flatpickr`) is globally available.
 */

document.addEventListener("DOMContentLoaded", function() {
    flatpickr("#specific_dates_picker", {
        mode: "multiple",
        dateFormat: "Y-m-d",
        allowInput: true,
    });
});
