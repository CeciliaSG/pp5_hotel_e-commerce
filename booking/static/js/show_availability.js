$(document).ready(function () {
    console.log("Document is ready");

    const serviceField = $('#id_service');
    const dateField = $('#id_date');

    dateField.datepicker({
        dateFormat: 'yy-mm-dd',
    });

    serviceField.change(function () {
        const selectedService = $(this).val();
        console.log("Service selected:", selectedService);

        if (selectedService) {
            $.ajax({
                url: `/booking/get-available-dates/${selectedService}/`,
                method: 'GET',
                success: function (data) {
                    console.log("Available dates fetched:", data);

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
                error: function (error) {
                    console.error('Error fetching available dates:', error);
                }
            });
        }
    });
});



