# [PC SHOP](https://pcshop-ff340fe41fef.herokuapp.com/)
==============

Developer: Md Minhazul Alam (https://github.com/Md-Minhazul-Alam)

Project Overview
----------------
This is an end-to-end e-commerce site for a PC shop built using Django (Python) as the backend
and a client-side responsive implementation using HTML, CSS, Bootstrap, and custom JavaScript. The platform
supports filter, product browsing, cart management, user profiles, and Stripe checkout.

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
- Product Categories
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


Database Schema
---------------

1. Website Settings

WebsiteSetting
- id (PK)
- website_name: Char(100)
- website_tagline: Char(100)
- website_description: Text
- website_logo: Image
- website_favicon: Image
- website_thumbnail: Image
- website_address: Char(255)
- website_contact_phone: Char(15)
- website_contact_email: Email
- website_office_hour: Text

QuickLink
- id (PK)
- title: Char(200)
- slug: Slug(200)
- description: HTMLField
- meta_keywords: Text
- meta_description: Text
- is_active: Boolean

LegalLink
- id (PK)
- title: Char(200)
- slug: Slug(200)
- description: HTMLField
- meta_keywords: Text
- meta_description: Text
- is_active: Boolean

2. Products

Tag
- id (PK)
- tag: Char(100)
- tag_slug: Slug(100)
- is_active: Boolean

Brand
- id (PK)
- brand: Char(100)
- brand_slug: Slug(100)
- brand_image: Image
- is_active: Boolean

Category
- id (PK)
- category: Char(100)
- category_slug: Slug(100)
- category_image: Image
- is_active: Boolean
- parent_category: FK → Category (self)

Variation
- id (PK)
- name: Char(100)
- value: Char(100)
- variation_slug: Slug(200)
- is_active: Boolean

Product
- id (PK)
- product_name: Char(200)
- product_slug: Slug(255)
- sku: Char(200)
- brand: FK → Brand
- category: FK → Category
- tags: ManyToMany → Tag
- price: Decimal(8,2)
- short_description: Char(255)
- description: HTMLField
- has_variation: Boolean
- rating: Decimal(6,2)
- image_url: URLField
- thumbnail: Image
- is_active: Boolean
- is_featured: Boolean
- created_at: DateTime
- updated_at: DateTime

ProductVariation
- id (PK)
- product: FK → Product
- variation: FK → Variation
- stock: PositiveInteger
- Unique Together: (product, variation)

3. Orders

Order
- id (PK)
- order_number: Char(32)
- user_profile: FK → UserProfile
- full_name: Char(50)
- email: Email
- phone_number: Char(20)
- country: CountryField
- postcode: Char(20)
- town_or_city: Char(40)
- street_address1: Char(80)
- street_address2: Char(80)
- county: Char(80)
- date: DateTime
- delivery_cost: Decimal
- order_total: Decimal
- grand_total: Decimal
- original_bag: Text
- stripe_pid: Char(254)

OrderLineItem
- id (PK)
- order: FK → Order
- product: FK → Product
- product_variation: Char(255)
- quantity: Integer
- lineitem_total: Decimal

4. User Profiles

UserProfile
- id (PK)
- user: OneToOne → User
- phone: Char(20)
- address_line1: Char(255)
- address_line2: Char(255)
- city: Char(100)
- state: Char(100)
- country: CountryField
- postal_code: Char(20)
- created_at: DateTime
- updated_at: DateTime

5. Sliders

HeroSlider
- id (PK)
- title: Char(100)
- subtitle: Char(200)
- image: Image
- link: URLField

------------------------------------------------------------
RELATIONSHIPS
------------------------------------------------------------

- Product → Brand: Many-to-One  
- Product → Category: Many-to-One  
- Product → Tag: Many-to-Many  
- Product → ProductVariation: One-to-Many  
- ProductVariation → Variation: Many-to-One  
- Order → OrderLineItem: One-to-Many  
- Order → UserProfile: Many-to-One  
- User → UserProfile: One-to-One  
- Category → Category: Self-referencing (parent category)


Notes
-----
- Images are uploaded to `/media/` directory
- TinyMCE is used for HTML content fields
- Stripe PID stored for payment tracking
- Order totals automatically calculate delivery cost based on free shipping threshold

Color Scheme
------------
- Primary: White (#FFFFFF)
- Text: Black (#000000)
- Accent: Blue (#3069a3)

Typography
----------
- Fonts: "DM Sans", sans-serif (Google Free Font)
- Icons: Font Awesome


Skeleton / Wireframes
--------------------
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



User Stories
------------
| Role | Action | Outcome |
|------|---------|----------|
| Visitor | Browse products by category | Find desired products easily |
| Visitor | Filter/sort products | View products by price, rating, or name |
| User | Add products to cart | Review selections and proceed to purchase |
| User | Checkout using Stripe | Secure and verified payment |
| User | Manage profile | Update info and view past orders |
| Admin | Manage products, categories, and orders | Maintain full control of shop content |


------------------------------------------------------------
FEATURES
------------------------------------------------------------

| SECTION             | DESCRIPTION                                                                                                     | Screenshot / Image                                       |
|---------------------|-----------------------------------------------------------------------------------------------------------------|----------------------------------------------------------|
| Header              | Top bar with free shipping message (left) and contact number (right). Main header with logo (left), search bar (center), cart & user icons (right). Cart icon shows product count. | ![Header](/static/screenshots/header.png)               |
| User Authentication | Login, signup, and password reset handled via Django Allauth. Displays “My Account” if logged in or “Login / Sign up” otherwise. | ![Auth](/static/screenshots/auth.png)                   |
| Hero Slider         | Displays running offers and promotions. Each slide links to a relevant category or product.                     | ![Slider](/static/screenshots/slider.png)               |
| Homepage Categories | Selected featured categories displayed as clickable cards that redirect to category listings.                  | ![Categories](/static/screenshots/categories.png)       |
| Featured Products   | Displays highlighted or exclusive products pulled dynamically from database.                                    | ![Featured Products](/static/screenshots/featured.png)  |
| Footer              | Four columns — (1) Logo & description, (2) Quick links, (3) Category links, (4) Legal pages.                   | ![Footer](/static/screenshots/footer.png)               |
| Category Page       | Shows products of a selected category with breadcrumbs. Includes filters: price (low→high / high→low), rating, and alphabetical (A→Z / Z→A). | ![Category](/static/screenshots/category.png)           |
| Product Details     | Product images (left), details (right): title, rating, price, short description, quantity selector, variation dropdown (if available), add to cart, and related products section. | ![Product Details](/static/screenshots/details.png)     |
| Add-to-Cart Popup   | Notification appears showing added items, subtotal, and free shipping progress bar.                             | ![Add-to-Cart](/static/screenshots/add_to_cart.png)     |
| Cart Page           | Displays items with plus/minus quantity controls and remove option. Right side shows order summary with total, delivery, and free shipping indicator. | ![Cart](/static/screenshots/cart.png)                   |
| Checkout Page       | Simple form with billing/shipping info, country dropdown, and Stripe payment form.                              | ![Checkout](/static/screenshots/checkout.png)           |
| Order Confirmation  | Success page showing order number, details, billing, and shipping info. Sends email confirmation.               | ![Order Success](/static/screenshots/success.png)       |
| User Profile        | Editable user info: name, phone, address, country. Lists past orders with date and total.                       | ![Profile](/static/screenshots/profile.png)             |
| Admin Panel         | Django Admin for full CRUD control on products, brands, categories, and orders.                                  | ![Admin](/static/screenshots/admin.png)                 |


Tools & Technologies
--------------------
- Django (Python) – Backend framework
- PostgreSQL – Database
- HTML/CSS/Bootstrap – Frontend styling
- JavaScript – Interactivity
- Stripe API – Payment gateway
- Django Allauth – Authentication
- Git & GitHub – Version control
- VSCode – Development IDE
- Font Awesome – Icons
- HackMD – For README / testing documentation

Agile Development
-----------------
- GitHub Projects & Issues for task management
- MoSCoW prioritization for features
- Responsiveness and functionality testing
- Used for Kanban style task management with epics and issues

Screenshot / Example:
![Agile Kanban](/static/screenshots/agile_kanban.png)

GitHub Issues
-------------
All reported errors, feature requests, and improvements were tracked through GitHub Issues.  
Common issues included model relationships, view routing bugs, and API response mismatches during integration with Stripe and Allauth.

MoSCoW Prioritization
---------------------
Must Have: Product CRUD, cart, checkout, and Stripe payment integration  
Should Have: User profile management and category filtering  
Could Have: Wishlist and product reviews  
Won’t Have: Discount coupons or referral system (planned for future release)

Testing
-------
All features were manually tested on desktop, tablet, and mobile for responsiveness and functionality.  
Stripe test mode was used for payment verification.  
User registration and login were validated through Django Allauth flows.  
Errors, test logs, and screenshots are documented separately in `TESTING.md`.

Deployment
----------
- Hosted on Purchased Hosting for testing
- Stripe payment integration active
- Email notifications for orders enabled

Local vs Deployment
-------------------
Minor differences may exist between the local and deployed versions due to environment settings, database connections, and API keys.

Local Development
-----------------
**Cloning the Repository**
1. Go to the GitHub repository.
2. Click the green **Code** button and copy the URL (HTTPS, SSH, or GitHub CLI).
3. Open Terminal or Git Bash and navigate to your desired project directory.
4. Run:  
   ```bash
   git clone <repository-url>

---

Future Features
---------------
- Dark mode toggle
- Wishlist/favorites
- Product reviews & ratings
- Discount coupons and promo codes

## Credits

### Content
| Source | Notes |
| --- | --- |
| ChatGPT | Helped debug and explain Django/JS issues |
| Claude AI | Helped debug and explain Django/JS issues |
| W3Schools | References for CSS/JS |
| Django Docs | Backend reference |

### Media
- [Google Images](https://images.google.com) → Product and promotional images  
- [Freepik](https://www.freepik.com) → Icons, mockups, and design elements  
- [Font Awesome](https://fontawesome.com) → Icons used across UI  

### Acknowledgements
- Django and open-source community for documentation and discussions.  
- Code Institute and online developer communities for guidance and testing insights.  


