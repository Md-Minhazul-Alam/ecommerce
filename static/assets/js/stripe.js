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

        // Collect billing info from form
        const fullName = document.getElementById('id_full_name').value.trim();
        const email = document.getElementById('id_email').value.trim();
        const phone = document.getElementById('id_phone_number').value.trim();
        const address1 = document.getElementById('id_street_address1').value.trim();
        const address2 = document.getElementById('id_street_address2').value.trim();
        const city = document.getElementById('id_town_or_city').value.trim();
        const state = document.getElementById('id_county').value.trim();
        const country = document.getElementById('id_country').value.trim();
        const postcode = document.getElementById('id_postcode').value.trim();
        const saveInfo = document.getElementById('id-save-info')?.checked || false;

        const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

        // Cache checkout data
        const postData = {
            csrfmiddlewaretoken: csrfToken,
            client_secret: clientSecret,
            save_info: saveInfo,
        };
        const url = '/checkout/cache_checkout_data/';

        try {
            await fetch(url, { method: 'POST', body: new URLSearchParams(postData) });

            // Confirm payment
            const { error, paymentIntent } = await stripe.confirmCardPayment(clientSecret, {
                payment_method: {
                    card: card,
                    billing_details: {
                        name: fullName || 'Unknown',
                        email: email || 'no-email@example.com',
                        phone: phone || '',
                        address: {
                            line1: address1 || '',
                            line2: address2 || '',
                            city: city || '',
                            state: state || '',
                            postal_code: postcode || '',
                            country: country || '',
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
            location.reload();
        }
    });
});

