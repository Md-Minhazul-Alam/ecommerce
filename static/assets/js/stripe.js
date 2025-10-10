// This script handles Stripe card payments.
// Docs: https://stripe.com/docs/payments/accept-a-payment

// --- Get Stripe keys from hidden HTML elements ---
let stripePublicKey = $('#id_stripe_public_key').text().trim().slice(1, -1);
let clientSecret = $('#id_client_secret').text().trim().slice(1, -1);

// --- Initialize Stripe ---
let stripe = Stripe(stripePublicKey);
let elements = stripe.elements();

// --- Style for the card input field ---
let cardStyle = {
    base: {
        color: '#000',
        fontFamily: 'Helvetica, sans-serif',
        fontSize: '16px',
        '::placeholder': { color: '#aab7c4' }
    },
    invalid: {
        color: '#dc3545',  // red color for errors
        iconColor: '#dc3545'
    }
};

// --- Create and mount the card input field ---
let card = elements.create('card', { style: cardStyle });
card.mount('#card-element');

// --- Show errors in real time when user types card info ---
card.addEventListener('change', (event) => {
    let errorDiv = document.getElementById('card-errors');

    if (event.error) {
        // Show the error message
        let errorHtml = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        errorDiv.innerHTML = errorHtml;
    } else {
        // No error
        errorDiv.textContent = '';
    }
});
