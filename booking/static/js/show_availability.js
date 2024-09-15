/**
 * This script initializes a date picker and dynamically updates available dates
 * based on the service selected by the user.
 * 
 * - The date picker is initially attached to the `#id_date` field with the format 'yy-mm-dd'.
 * - When the service in `#id_service` is changed, an AJAX request is triggered to fetch
 *   available dates for the selected service.
 * - Upon successful retrieval of available dates, the date picker is refreshed with 
 *   new minimum and maximum dates, and only the available dates are enabled for selection.
 * - If the service is not selected or an error occurs, no updates to the date picker are made.
 */
$(document).ready(function () {

    const serviceField = $('#id_service');
    const dateField = $('#id_date');

    dateField.datepicker({
        dateFormat: 'yy-mm-dd',
    });

    serviceField.change(function () {
        const selectedService = $(this).val();

        if (selectedService) {
            $.ajax({
                url: `/booking/get-available-dates/${selectedService}/`,
                method: 'GET',
                success: function (data) {
                    const availableDates = data.available_dates;
                    const minDate = data.min_date;
                    const maxDate = data.max_date;

                    dateField.datepicker("destroy").datepicker({
                        dateFormat: 'yy-mm-dd',
                        minDate: new Date(minDate),
                        maxDate: new Date(maxDate),
                        beforeShowDay: function (date) {
                            const dateString = $.datepicker.formatDate('yy-mm-dd', date);
                            if (availableDates.indexOf(dateString) !== -1) {
                                return [true, "available-date", "Available"];
                            } else {
                                return [false, "", "Unavailable"];
                            }
                        }
                    });
                },
                error: function () {
                }
            });
        }
    });
});
