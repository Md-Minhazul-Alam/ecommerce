# Testing

[Return to README.md](README.md)

## Code Validation

All HTML and Django template files were validated using the [W3C HTML Validator](https://validator.w3.org) to ensure clean and accessible markup.  
Minor warnings related to Django template tags (`{% %}` / `{{ }}`) were ignored as they are not standard HTML.

| Page             | Template File                          | Screenshot                                           |
| ---------------- | -------------------------------------- | ---------------------------------------------------- |
| Home Page        | `templates/home/index.html`             | ![Home](/static/testing/html-home.png)               |
| Product Listing  | `templates/product/category.html`       | ![Category](/static/testing/html-category.png)       |
| Product Details  | `templates/product/product_detail.html` | ![Details](/static/testing/html-details.png)         |
| Cart Page        | `templates/bag/bag.html`                | ![Cart](/static/testing/html-cart.png)               |
| Checkout Page    | `templates/checkout/checkout.html`      | ![Checkout](/static/testing/html-checkout.png)       |
| Order Success    | `templates/checkout/order_success.html` | ![Success](/static/testing/html-success.png)         |
| Profile Page     | `templates/profiles/profile.html`       | ![Profile](/static/testing/html-profile.png)         |
| Legal Page         | `templates/businessprofile/legal_link_detail.html`               | ![Legal](/static/testing/html-legal.png)                 |
| Quick Page         | `templates/businessprofile/quick_link_detail.html`               | ![Quick](/static/testing/html-quick.png)                 |


## CSS Validation

All CSS files were validated using the [W3C CSS Validator](https://jigsaw.w3.org/css-validator) to ensure proper syntax and browser compatibility.  
Minor warnings related to vendor prefixes were ignored as they enhance cross-browser support.

| CSS File                                       | Template Files                                                                                                        | Screenshot                                         |
| ---------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| `static/assets/css/style.css`                  | `templates/home/index.html`, `templates/product/category.html`, `templates/product/product_detail.html`, `templates/home/404.html` | ![style.css Validation](/static/testing/css-style.png) |
| `static/assets/css/profile.css`                | `templates/profiles/profile.html`                                                                                     | ![profile.css Validation](/static/testing/css-profile.png) |
| `static/assets/css/checkout.css`               | `templates/checkout/checkout.html`, `templates/checkout/order_success.html`, `templates/bag/bag.html`                 | ![checkout.css Validation](/static/testing/css-checkout.png) |


## JS Validation  

All JavaScript files were validated using [JSHint](https://jshint.com/) to ensure clean, maintainable, and error-free code.  
Minor warnings related to ES6 syntax and Stripe API functions were ignored as they are intentional.

| Location                     | File / Purpose                                 | Screenshot                                         |
| ----------------------------- | ---------------------------------------------- | ------------------------------------------------- |
| `static/assets/js/main.js`    | Handles site-wide interactivity: menu toggle, cart updates, and dynamic UI elements | ![main.js Validation](/static/testing/js-main.png) |
| `static/assets/js/stripe.js`  | Manages Stripe payment integration on checkout page | ![stripe.js Validation](/static/testing/js-stripe.png) |


## Responsiveness

Tested on desktop, tablet, and mobile devices.

| Page             | Description                                   | Desktop Screenshot                         | Tablet Screenshot                          | Mobile Screenshot                          |
|------------------|-----------------------------------------------|-------------------------------------------|--------------------------------------------|--------------------------------------------|
| Home Page        | Header, slider, categories, featured products, footer | ![Home Desktop](/static/screenshots/home.png) | ![Home Tablet](/static/screenshots/home_tablet.png) | ![Home Mobile](/static/screenshots/home_mobile.png) |
| Product Listing  | Product grid, filters, sorting, pagination   | ![Listing Desktop](/static/screenshots/listing.png) | ![Listing Tablet](/static/screenshots/listing_tablet.png) | ![Listing Mobile](/static/screenshots/listing_mobile.png) |
| Product Details  | Image gallery, title, price, description, variations, add to cart | ![Details Desktop](/static/screenshots/details.png) | ![Details Tablet](/static/screenshots/details_tablet.png) | ![Details Mobile](/static/screenshots/details_mobile.png) |
| Cart Page        | Selected items, quantity update, order summary | ![Cart Desktop](/static/screenshots/cart.png) | ![Cart Tablet](/static/screenshots/cart_tablet.png) | ![Cart Mobile](/static/screenshots/cart_mobile.png) |
| Checkout Page    | Shipping & billing forms, Stripe payment, summary | ![Checkout Desktop](/static/screenshots/checkout.png) | ![Checkout Tablet](/static/screenshots/checkout_tablet.png) | ![Checkout Mobile](/static/screenshots/checkout_mobile.png) |
| Order Success    | Confirmation, order summary, email notification | ![Success Desktop](/static/screenshots/success.png) | ![Success Tablet](/static/screenshots/success_tablet.png) | ![Success Mobile](/static/screenshots/success_mobile.png) |
| User Profile     | Profile update, order history                 | ![Profile Desktop](/static/screenshots/profile.png) | ![Profile Tablet](/static/screenshots/profile_tablet.png) | ![Profile Mobile](/static/screenshots/profile_mobile.png) |
| 404 Page         | Show Page not Found                           | ![404 Desktop](/static/screenshots/404.png) | ![404 Tablet](/static/screenshots/404_tablet.png) | ![404 Mobile](/static/screenshots/404_mobile.png) |


## Browser Compatibility

The site was tested on Chrome and Firefox to ensure consistent layout, styling, and interactivity.  
All features, including Stripe payment, cart management, and responsive navigation, performed as expected.

| Page             | Chrome Screenshot                                                                 | Firefox Screenshot                                                                | Notes             |
| ---------------- | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | ----------------- |
| Home Page        | ![Chrome Home](/static/testing/browser/chrome/chrome-home.png)                   | ![Firefox Home](/static/testing/browser/firefox/firefox-home.png)                 | Works as expected |
| Product Listing  | ![Chrome Listing](/static/testing/browser/chrome/chrome-category.png)            | ![Firefox Listing](/static/testing/browser/firefox/firefox-category.png)          | Works as expected |
| Product Details  | ![Chrome Details](/static/testing/browser/chrome/chrome-details.png)              | ![Firefox Details](/static/testing/browser/firefox/firefox-details.png)           | Works as expected |
| Cart Page        | ![Chrome Cart](/static/testing/browser/chrome/chrome-cart.png)                    | ![Firefox Cart](/static/testing/browser/firefox/firefox-cart.png)                 | Works as expected |
| Checkout Page    | ![Chrome Checkout](/static/testing/browser/chrome/chrome-checkout.png)            | ![Firefox Checkout](/static/testing/browser/firefox/firefox-checkout.png)         | Works as expected |
| Order Success    | ![Chrome Success](/static/testing/browser/chrome/chrome-success.png)              | ![Firefox Success](/static/testing/browser/firefox/firefox-success.png)           | Works as expected |
| Profile Page     | ![Chrome Profile](/static/testing/browser/chrome/chrome-profile.png)              | ![Firefox Profile](/static/testing/browser/firefox/firefox-profile.png)           | Works as expected |
| 404 Page         | ![Chrome 404](/static/testing/browser/chrome/chrome-404.png)                      | ![Firefox 404](/static/testing/browser/firefox/firefox-404.png)                   | Works as expected |
| Quick Links       | ![Chrome Quick](/static/testing/browser/chrome/chrome-quick.png)                      | ![Firefox Quick](/static/testing/browser/firefox/firefox-quick.png)                   | Works as expected |
| Legal Page         | ![Chrome Legal](/static/testing/browser/chrome/chrome-legal.png)                      | ![Firefox Legal](/static/testing/browser/firefox/firefox-legal.png)                   | Works as expected |


