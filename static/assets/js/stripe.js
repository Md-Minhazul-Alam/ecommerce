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
            invalid: { color: '#dc3545', iconColor: '#dc3545' },
        },
    });
    card.mount('#card-element');

    const form = document.getElementById('payment-form');
    const errorDiv = document.getElementById('card-errors');
    const submitBtn = document.getElementById('submit-button');
    const loader = document.getElementById('loader-overlay');

    card.addEventListener('change', (event) => {
        errorDiv.innerHTML = event.error
            ? `<span class="icon" role="alert"><i class="fas fa-times"></i></span> <span>${event.error.message}</span>`
            : '';
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        submitBtn.disabled = true;
        card.update({ disabled: true });

        // Show loader
        loader.classList.remove('d-none');

        const { error, paymentIntent } = await stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
            }
        });

        if (error) {
            errorDiv.innerHTML = `
                <span class="icon" role="alert"><i class="fas fa-times"></i></span>
                <span>${error.message}</span>
            `;
            submitBtn.disabled = false;
            card.update({ disabled: false });
            loader.classList.add('d-none'); // hide loader
        } else if (paymentIntent.status === 'succeeded') {
            form.submit();
        }
    });
});
