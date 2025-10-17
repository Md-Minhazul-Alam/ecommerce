// Stripe Payment Handling
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

    const cardStyle = {
        base: { color: '#000', fontFamily: 'Helvetica, sans-serif', fontSize: '16px', '::placeholder': { color: '#aab7c4' } },
        invalid: { color: '#dc3545', iconColor: '#dc3545' },
    };

    const card = elements.create('card', { style: cardStyle });
    card.mount('#card-element');

    const form = document.getElementById('payment-form');
    const errorDiv = document.getElementById('card-errors');
    const submitBtn = document.getElementById('submit-button');
    const loader = document.getElementById('loader-overlay');

    card.addEventListener('change', (event) => {
        if (event.error) {
            errorDiv.innerHTML = `<span class="icon" role="alert"><i class="fas fa-times"></i></span>
                                  <span>${event.error.message}</span>`;
        } else {
            errorDiv.textContent = '';
        }
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        submitBtn.disabled = true;
        card.update({ disabled: true });
        loader.classList.remove('d-none');

        // Collect form data using the actual form inputs
        // Django crispy forms creates inputs with names matching the model fields
        const fullName = document.querySelector('input[name="full_name"]')?.value.trim() || '';
        const email = document.querySelector('input[name="email"]')?.value.trim() || '';
        const phone = document.querySelector('input[name="phone_number"]')?.value.trim() || '';
        const address1 = document.querySelector('input[name="street_address1"]')?.value.trim() || '';
        const address2 = document.querySelector('input[name="street_address2"]')?.value.trim() || '';
        const city = document.querySelector('input[name="town_or_city"]')?.value.trim() || '';
        const state = document.querySelector('input[name="county"]')?.value.trim() || '';
        const country = document.querySelector('select[name="country"]')?.value.trim() || '';
        const postcode = document.querySelector('input[name="postcode"]')?.value.trim() || '';
        const saveInfo = document.querySelector('input[name="save-info"]')?.checked || false;

        const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

        // Cache checkout data - NOW WITH ALL FORM FIELDS!
        const postData = new URLSearchParams({
            csrfmiddlewaretoken: csrfToken,
            client_secret: clientSecret,
            save_info: saveInfo,
            full_name: fullName,
            email: email,
            phone_number: phone,
            street_address1: address1,
            street_address2: address2,
            town_or_city: city,
            county: state,
            country: country,
            postcode: postcode,
        });

        const url = '/checkout/cache_checkout_data/';

        try {
            const cacheResponse = await fetch(url, { 
                method: 'POST', 
                body: postData
            });

            if (!cacheResponse.ok) {
                console.warn('Cache checkout data warning:', cacheResponse.status);
            }

            // Confirm payment
            const { error, paymentIntent } = await stripe.confirmCardPayment(clientSecret, {
                payment_method: {
                    card: card,
                    billing_details: {
                        name: fullName,
                        email: email,
                        phone: phone,
                        address: {
                            line1: address1,
                            line2: address2,
                            city: city,
                            state: state,
                            postal_code: postcode,
                            country: country,
                        }
                    }
                },
                shipping: {
                    name: fullName,
                    phone: phone,
                    address: {
                        line1: address1,
                        line2: address2,
                        city: city,
                        state: state,
                        postal_code: postcode,
                        country: country,
                    }
                }
            });

            // Handle errors or success
            if (error) {
                errorDiv.innerHTML = `<span class="icon" role="alert"><i class="fas fa-times"></i></span>
                                      <span>${error.message}</span>`;
                submitBtn.disabled = false;
                card.update({ disabled: false });
                loader.classList.add('d-none');
            } else if (paymentIntent.status === 'succeeded') {
                form.submit();
            }

        } catch (err) {
            console.error('Checkout error:', err);
            location.reload();
        }
    });
});