// Stripe payment handling
// Docs: https://stripe.com/docs/payments/accept-a-payment

document.addEventListener("DOMContentLoaded", () => {
    const stripePublicKey = document.getElementById('id_stripe_public_key')?.textContent.trim().slice(1, -1);
    const clientSecret = document.getElementById('id_client_secret')?.textContent.trim().slice(1, -1);

    if (!stripePublicKey || !clientSecret) {
        console.error("Stripe keys missing from template.");
        return;
    }

    const stripe = Stripe(stripePublicKey);
    const elements = stripe.elements();

    const card = elements.create('card', {
        style: {
            base: {
                color: '#000',
                fontFamily: 'Helvetica, sans-serif',
                fontSize: '16px',
                '::placeholder': { color: '#aab7c4' },
            },
            invalid: {
                color: '#dc3545',
                iconColor: '#dc3545',
            },
        },
    });

    card.mount('#card-element');

    const form = document.getElementById('payment-form');
    const errorDiv = document.getElementById('card-errors');
    const submitBtn = document.getElementById('submit-button');

    // Show errors
    card.addEventListener('change', (event) => {
        errorDiv.innerHTML = event.error
            ? `<span class="icon" role="alert"><i class="fas fa-times"></i></span> <span>${event.error.message}</span>`
            : '';
    });

    // Handle form submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        submitBtn.disabled = true;
        card.update({ disabled: true });

        const { error, paymentIntent } = await stripe.confirmCardPayment(clientSecret, {
            payment_method: { card },
        });

        if (error) {
            errorDiv.innerHTML = `
                <span class="icon" role="alert"><i class="fas fa-times"></i></span>
                <span>${error.message}</span>
            `;
            submitBtn.disabled = false;
            card.update({ disabled: false });
        } else if (paymentIntent.status === 'succeeded') {
            form.submit();
        }
    });
});
