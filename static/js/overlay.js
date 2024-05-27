function openOverlay(event) {
    event.preventDefault();

    document.getElementById("cart-overlay").style.display = "block";

    fetch("/cart/")
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();
        })
        .then(data => {
            console.log("Fetched cart data:", data); 
            document.getElementById("modal").innerHTML = data;
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function closeOverlay() {
    document.getElementById("cart-overlay").style.display = "none";
}