PC Shop Django
==============

Developer: Md Minhazul Alam (https://github.com/Md-Minhazul-Alam)

Project Overview
----------------
This is a full-stack e-commerce platform for a PC shop built with Django (Python) as the backend
and a responsive frontend using HTML, CSS, Bootstrap, and custom JavaScript. The platform
supports browsing products, filtering, cart management, checkout with Stripe, and user profiles.

The goal is to provide a complete PC shopping experience with responsive design and real-world
functionality.

UX Strategy
-----------
Purpose:
- Demonstrate Django development skills.
- Provide an intuitive shopping experience.
- Act as a portfolio project.

Primary User Needs:
- Browse products by category, popularity, or offers.
- View product details, variations, and pricing.
- Add/remove products from cart and checkout securely.
- Manage personal profile and view order history.

Business Goals:
- Showcase full-stack development capability.
- Provide real-world e-commerce functionality.
- Serve as a learning and portfolio project.

Scope & Features
----------------
Homepage:
- Header with top bar (free shipping info, contact number)
- Logo, search bar, cart icon, user account/login toggle
- Offer slider for promotions
- Selected category sections
- Featured products section
- Footer: logo/description, quick links, categories, legal pages

Product Page:
- Product grid filtered by category
- Breadcrumbs navigation
- Filtering & sorting (price, rating, name)
- Pagination

Product Details Page:
- Image gallery
- Product title, rating, price
- Short description
- Quantity input & variations dropdown
- Add to cart button
- Related products
- Notification for cart additions and free shipping info

Cart Page:
- Cart items list
- Quantity update & remove items
- Order summary with total, shipping, and free shipping indicator
- Continue shopping / proceed to checkout buttons

Checkout Page:
- Shipping & billing form
- Country selection
- Stripe payment integration
- Traditional payment option
- Order summary & total

Order Success Page:
- Confirmation message
- Order items & details
- Shipping & billing info
- Email notification

User Profile:
- Update personal info, addresses, country, phone
- View order history

Authentication:
- Django Allauth: login, signup, password reset

