/*
    From Boutique Ado walk through: 
    
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment

*/

/* global Stripe */


$(document).ready(function() {
    let stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
    let clientSecret = $('#id_client_secret').text().slice(1, -1);
    let stripe = Stripe(stripePublicKey);
    let elements = stripe.elements();
    let style = {
        base: {
            color: '#191521',
            fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
            fontSmoothing: 'antialiased',
            fontSize: '16px',
            '::placeholder': {
                color: '#538991'
            }
        },
        invalid: {
            color: '#dc3545',
            iconColor: '#dc3545'
        }
    };
    let card = elements.create('card', { style: style });
    card.mount('#card-element');

    card.addEventListener('change', function(event) {
        let errorDiv = document.getElementById('card-errors');
        if (event.error) {
            let html = `
                <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                </span>
                <span>${event.error.message}</span>
            `;
            $(errorDiv).html(html);
        } else {
            errorDiv.textContent = '';
        }
    });

    let form = document.getElementById('payment-form');
    form.addEventListener('submit', function(ev) {
        ev.preventDefault();
        
        card.update({ 'disabled': true });
        $('#submit-button').attr('disabled', true);

        let saveInfo = Boolean($('#save-info').attr('checked'));
        let csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
        let postData = {
            'csrfmiddlewaretoken': csrfToken,
            'client_secret': clientSecret,
            'save_info': saveInfo,
        };
        let url = '/checkout/cache_checkout_data/';

        $.post(url, postData).done(function() {
            stripe.confirmCardPayment(clientSecret, {
                payment_method: {
                    card: card,
                    billing_details: {
                        name: $.trim(form.customer_name.value),
                        phone: $.trim(form.phone_number.value),
                        email: $.trim(form.email.value),
                    }
                }
            }).then(function(result) {
                if (result.error) {
                    let errorDiv = document.getElementById('card-errors');
                    let html = `
                        <span class="icon" role="alert">
                            <i class="fas fa-times"></i>
                        </span>
                        <span>${result.error.message}</span>`;
                    $(errorDiv).html(html);
                    card.update({ 'disabled': false });
                    $('#submit-button').attr('disabled', false);
                } else {
                    if (result.paymentIntent.status === 'succeeded') {
                        form.submit();
                    }
                }
            });
        });
    });
});
