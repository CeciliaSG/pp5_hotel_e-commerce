/**
 * This script dynamically updates available time slots for a selected spa service
 * and date. It provides graceful error handling and user feedback in case of 
 * invalid selections or issues fetching time slots.
 * 
 * - The spa service and date dropdowns trigger an update to the available time slots
 *   through an AJAX request.
 * - The time slots are dynamically inserted into the DOM as checkboxes, allowing users
 *   to select available slots, with booked slots being disabled.
 * - If the AJAX request fails or no time slots are available, the user is shown a
 *   clear error message.
 * - Handles cases where no time slots are available or where the service or date 
 *   selection is invalid.
 * 
 * Key Functions:
 * - `loadTimeSlots(spaServiceId, dateId)`: Fetches time slots for the selected service 
 *   and date, updates the UI, and attaches event listeners to handle selections.
 * - `showErrorMessage(message)`: Displays an error message in the UI and hides the "Save" 
 *   button if something goes wrong.
 * 
 * Events:
 * - The `spaServiceDropdown` changes reload the page to show the correct service.
 * - The `dateDropdown` triggers the `loadTimeSlots()` function to fetch and display 
 *   available time slots.
 * 
 * Graceful Error Handling:
 * - Provides user-friendly error messages for issues such as invalid service or date 
 *   selections, or problems fetching time slots from the server.
 */


document.addEventListener('DOMContentLoaded', function () {
    let spaServiceDropdown = document.getElementById('spa_service');
    let dateDropdown = document.getElementById('id_specific_date');
    let container = document.getElementById('time-slots-container');
    let saveButton = document.getElementById('save-button');

    function showErrorMessage(message) {
        const errorMessage = document.createElement('p');
        errorMessage.textContent = message;
        errorMessage.style.color = 'red';
        container.innerHTML = '';
        container.appendChild(errorMessage);
        saveButton.style.display = 'none';
    }

    function loadTimeSlots(spaServiceId, dateId) {
        let url = container.getAttribute('data-url')
            .replace('availability.id', spaServiceId);
        
        if (url && dateId) {
            fetch(url + "?date_id=" + dateId)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`Failed to fetch data. Status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    container.innerHTML = '';

                    if (data.time_slots.length === 0) {
                        showErrorMessage('No available time slots for the selected date.');
                        return;
                    }

                    data.time_slots.forEach(function (time_slot) {
                        let checked = (time_slot.is_available || time_slot.is_booked) ? 'checked' : '';
                        let checkboxClass = time_slot.is_booked ? 'booked-checkbox' : '';

                        container.innerHTML += `
                            <div>
                                <label>
                                    <input 
                                        type="checkbox" 
                                        name="time_slots" 
                                        value="${time_slot.time_slot__id}" 
                                        ${checked} 
                                        class="${checkboxClass}" 
                                        ${time_slot.is_booked ? 'disabled' : ''}
                                    >
                                    ${time_slot.time_slot__time}
                                </label>
                            </div>`;
                    });

                    document.querySelectorAll('input[type="checkbox"]')
                        .forEach(function(checkbox) {
                            checkbox.addEventListener('change', function() {
                                if (!checkbox.checked) {
                                    const hiddenInput = document.createElement('input');
                                    hiddenInput.type = 'hidden';
                                    hiddenInput.name = 'unchecked_time_slots';
                                    hiddenInput.value = checkbox.value;
                                    container.appendChild(hiddenInput);
                                }
                            });
                    });

                    container.style.display = 'block';
                    saveButton.style.display = 'block';
                })
                .catch(error => {
                    showErrorMessage('Error loading available time slots. Please try again later.');
                });
        } else {
            showErrorMessage('Invalid service or date selected. Please try again.');
        }
    }

    spaServiceDropdown.addEventListener('change', function () {
        let selectedSpaServiceId = this.value;
        window.location.href = '?spa_service=' + selectedSpaServiceId;
    });

    dateDropdown.addEventListener('change', function () {
        let selectedDateId = this.value;
        if (selectedDateId) {
            loadTimeSlots(spaServiceDropdown.value, selectedDateId);
        }
    });

    if (spaServiceDropdown.value && dateDropdown.value) {
        loadTimeSlots(spaServiceDropdown.value, dateDropdown.value);
    }
});
