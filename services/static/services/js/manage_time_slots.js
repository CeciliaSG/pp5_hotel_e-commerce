document.addEventListener('DOMContentLoaded', function () {
    console.log('Event listener attached');
    let spaServiceDropdown = document.getElementById('spa_service');
    let dateDropdown = document.getElementById('id_specific_date');
    let container = document.getElementById('time-slots-container');

    function loadTimeSlots(spaServiceId, dateId) {
        let url = container.getAttribute('data-url').replace('availability.id', spaServiceId);
        if (url && dateId) {
            console.log('Making fetch request to:', url + "?date_id=" + dateId);
            fetch(url + "?date_id=" + dateId)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    console.dir(data);
                    console.log('Received data:', data);
                    container.innerHTML = '';

                    data.time_slots.forEach(function (time_slot) {
                        let checked = time_slot.is_available || time_slot.is_booked ? 'checked' : '';
                        let checkboxClass = time_slot.is_booked ? 'booked-checkbox' : '';

                        container.innerHTML += `
                            <div>
                                <label>
                                    <input type="checkbox" name="time_slots" value="${time_slot.time_slot__id}" ${checked} class="${checkboxClass}" ${time_slot.is_booked ? 'disabled' : ''}>
                                    ${time_slot.time_slot__time}
                                </label>
                            </div>`;
                    });
                    container.style.display = 'block';

                    let bookedCheckboxes = document.querySelectorAll('.booked-checkbox');
                    bookedCheckboxes.forEach(function(checkbox) {
                        checkbox.style.accentColor = 'red';
                        if (checkbox.checked) {
                            checkbox.style.backgroundColor = 'red';
                            checkbox.style.borderColor = 'red';
                        }
                    });
                })
                .catch(error => {
                    console.error('Error fetching time slots:', error);
                });
        } else {
            console.error('Invalid URL or Date ID');
        }
    }

    spaServiceDropdown.addEventListener('change', function () {
        let selectedSpaServiceId = this.value;
        window.location.href = '?spa_service=' + selectedSpaServiceId;
    });

    dateDropdown.addEventListener('change', function () {
        let selectedDateId = this.value;
        loadTimeSlots(spaServiceDropdown.value, selectedDateId);
    });

    if (spaServiceDropdown.value && dateDropdown.value) {
        loadTimeSlots(spaServiceDropdown.value, dateDropdown.value);
    }
});
