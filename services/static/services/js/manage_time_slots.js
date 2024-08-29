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
                        let checked = time_slot.is_available ? 'checked' : '';
                        let redCheck = time_slot.is_booked ? 'style="color:red;"' : '';

                        container.innerHTML += `
                            <div>
                                <label ${redCheck}>
                                    <input type="checkbox" name="time_slots" value="${time_slot.time_slot__id}" ${checked}>
                                    ${time_slot.time_slot__time}
                                </label>
                            </div>`;
                    });
                    container.style.display = 'block';
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
