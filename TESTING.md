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


## Lighthouse Audit

Audited with Lighthouse for performance, accessibility, SEO, and best practices.

| Page                                | Desktop Screenshot                                                        | Mobile Screenshot                                                        |
| ----------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| Home Page                            | ![Home Desktop](/static/testing/lighthouse/light-desktop-home.png)        | ![Home Mobile](/static/testing/lighthouse/light-mobile-home.png)         |
| Product Listing / Category Page      | ![Category Desktop](/static/testing/lighthouse/light-desktop-category.png) | ![Category Mobile](/static/testing/lighthouse/light-mobile-category.png) |
| Product Details Page                 | ![Details Desktop](/static/testing/lighthouse/light-desktop-details.png)   | ![Details Mobile](/static/testing/lighthouse/light-mobile-details.png)   |
| Cart Page                            | ![Cart Desktop](/static/testing/lighthouse/light-desktop-cart.png)         | ![Cart Mobile](/static/testing/lighthouse/light-mobile-cart.png)         |
| Checkout Page                        | ![Checkout Desktop](/static/testing/lighthouse/light-desktop-checkout.png) | ![Checkout Mobile](/static/testing/lighthouse/light-mobile-checkout.png) |
| User Profile Page                     | ![Profile Desktop](/static/testing/lighthouse/light-desktop-profile.png)   | ![Profile Mobile](/static/testing/lighthouse/light-mobile-profile.png)   |
| About / Contact / Privacy Policy     | ![Page Desktop](/static/testing/lighthouse/light-desktop-page.png)         | ![Page Mobile](/static/testing/lighthouse/light-mobile-page.png)         |
| Search Page                          | ![Search Desktop](/static/testing/lighthouse/light-desktop-search.png)     | ![Search Mobile](/static/testing/lighthouse/light-mobile-search.png)     |


---

## Defensive Programming

| Feature           | Expectation                                   | Test                                         | Result                 | Screenshot                                                                                  |
| ----------------- | --------------------------------------------- | ------------------------------------------- | ---------------------- | ------------------------------------------------------------------------------------------- |
| Navigation bar    | Adaptive on desktop, tablet, mobile          | Tested all device widths                     | Works consistently     | ![Navbar Desktop](/static/testing/features/navbar.png) ![Navbar Mobile](/static/testing/features/mobile-navbar.png) |
| Hero / Offer slider| Displays current promotions correctly        | Checked slider for active promotions        | Works as expected      | ![Hero Slider](/static/testing/features/sliders.png)                                        |
| Product Listing   | Displays products correctly with filters     | Checked categories, sorting, and pagination | Works as expected      | ![Product Listing](/static/testing/features/product-listing.png)                             |
| Product search    | Filters products by name, price, rating      | Entered test search terms                    | Correct products listed | ![Search Modal](/static/testing/features/search.png) ![Search Results](/static/testing/features/search-result.png) |
| Cart functionality| Add/remove/update quantity, calculate totals | Added multiple products, changed quantity   | Totals update correctly | ![Cart Function](/static/testing/features/cart-update.png)                                   |
| Checkout process  | Stripe payment and order summary correct      | Completed test checkout                      | Payment succeeds       | ![Checkout](/static/testing/features/checkout.png)                                          |
| Profile update    | Update personal info and view orders         | Edited profile info, viewed past orders     | Changes saved correctly | ![Profile](/static/testing/features/profile.png)                                           |

# PC SHOP - User Story Testing

This file documents all user story tests for the PC Shop e-commerce project, including steps, expected results, and screenshots for verification.

---

## User Story Testing

| User Story | Steps | Expected Result | Screenshot |
| ---------- | ----- | --------------- | ---------- |
| **Browse Products** | 1. Open Home Page<br>2. Click on a category | Products of selected category are displayed | ![Home](/static/testing/user-story/home.png) |
| **Filter / Sort Products** | 1. Go to Product Listing<br>2. Apply price/rating/name filter | Products are correctly filtered/sorted | ![Filter](/static/testing/user-story/filter.png) |
| **Select Product Variation** | 1. Open Product Details<br>2. Select variation from dropdown | Selected variation is displayed; price updates if applicable | ![Variation](/static/testing/user-story/variation.png) |
| **Adjust Quantity** | 1. On Product Details or Cart<br>2. Increase/decrease quantity | Quantity updates; line total recalculates correctly | ![Quantity](/static/testing/user-story/quantity.png) |
| **Add to Cart** | 1. Select variation & quantity<br>2. Click “Add to Cart” | Cart updates with correct product, variation, quantity, subtotal | ![Add to Cart](/static/testing/user-story/add-to-cart.png) |
| **Cart Management** | 1. Open Cart Page<br>2. Increase/decrease quantity, remove items | Cart updates totals and item list correctly | ![Cart](/static/testing/user-story/cart.png) |
| **Checkout Validation** | 1. Proceed to Checkout<br>2. Leave required fields empty<br>3. Attempt to submit | Warning messages displayed; checkout blocked | ![Checkout Validation](/static/testing/user-story/checkout-validation.png) |
| **Successful Checkout** | 1. Fill all required fields<br>2. Complete Stripe payment | Order processed; confirmation page displayed; email sent | ![Checkout Success](/static/testing/user-story/checkout-success.png) |
| **Profile Update** | 1. Open Profile Page<br>2. Update personal info<br>3. Save changes | Updated info saved; reflected immediately | ![Profile Update](/static/testing/user-story/profile-update.png) |
| **Quick & Legal Links** | 1. Click Quick/Legal link in Footer | Opens correct page in new tab | ![Quick Link](/static/testing/user-story/quick-link.png) |

---

## Notes

- All required fields on Checkout and Profile pages must be validated.
- Cart totals should recalculate correctly when quantities are adjusted.
- Screenshots should be updated whenever UI changes occur.
- Additional device-specific testing (desktop, tablet, mobile) can be added in separate columns if needed.
- Previously, I had deployed my project on my purchased hosting because I was facing issues with Heroku. However, I was unable to submit the assessment using that link. Therefore, I had to redeploy the project on Heroku for the assessment, which required editing several files in the project. Here is the link from the previous deployment for your reference.
- https://pcshop.zpos.top/


## Bugs

* **Automated email notifications not sending correctly in some environments**  
  **Fix:** Ensure SMTP credentials and Django email backend are properly configured → Done 

* **Minor layout misalignment on mobile for cart and checkout pages**  
  **Fix:** Adjusted CSS flex/grid rules and media queries → Resolved  

* **Product variation dropdown not updating quantity correctly**  
  **Fix:** Added JS fallback logic → Resolved  

* **Quick links or legal links sometimes display empty if inactive**  
  **Fix:** Added conditional rendering in templates → Resolved  

* **Hero slider images not scaling properly on small screens**  
  **Fix:** Added responsive image classes and object-fit → Resolved  

---

## Known Issues

* Automated email notifications may still fail in local development if SMTP server is not running.  
* Minor responsive issues may appear in very small screen widths (<320px) — non-critical.
