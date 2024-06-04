/*
    From Boutique Ado walk through: 
    
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment

    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

 $(document).ready(function() {
        let stripe_public_key = $('#id_stripe_public_key').text().slice(1, -1);
        let client_secret = $('#id_client_secret').text().slice(1, -1);
        let stripe = Stripe(stripe_public_key);
        let elements = stripe.elements();
        let style = {
            base: {
                color: '#191521',
                fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
                fontSmoothing: 'antialiased',
                fontSize: '16px',
                '::placeholder': {
                    color: '#191521'
                }
            },
            invalid: {
                color: '#dc3545',
                iconColor: '#dc3545'
            }
        };
        let card = elements.create('card', {style: style});
        card.mount('#card-element');
});