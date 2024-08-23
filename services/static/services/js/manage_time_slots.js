document.getElementById('id_specific_date').addEventListener('change', function() {
    let dateId = this.value;
    let container = document.getElementById('time-slots-container');
    let url = container.getAttribute('data-url');

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
                data.time_slots.forEach(function(time_slot) {
                    if (time_slot.time_slot__id && time_slot.time_slot__time) {
                        let checked = time_slot.is_available ? 'checked' : '';
                        container.innerHTML += `
                            <div>
                                <label>
                                    <input type="checkbox" name="time_slots" value="${time_slot.time_slot__id}" ${checked}>
                                    ${time_slot.time_slot__time}
                                </label>
                            </div>`;
                    } else {
                        console.error('Time slot data is incomplete:', time_slot);
                    }
                });
            })
            .catch(error => {
                console.error('Error fetching time slots:', error);
            });
    } else {
        console.error('Invalid URL or Date ID');
    }
});

