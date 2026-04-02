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

---

## Accessibility

The application has been designed with accessibility in mind to meet WCAG guidelines and ensure an inclusive user experience:

- ARIA labels added to all interactive elements including navigation, forms, buttons, and search bar
- Alt text provided on all product and site images for screen reader compatibility
- Semantic HTML elements used throughout the application (nav, main, section, article, footer)
- Responsive design tested and verified on desktop, tablet, and mobile screen sizes
- Color contrast meets WCAG accessibility guidelines
- Keyboard navigable interface throughout the site
- Form labels and input fields properly associated for screen reader support
- Error messages displayed clearly for form validation feedback

---

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
- Customer reviews with star rating and comment
- Submit, edit, and delete own review (signed-in users only)
- Duplicate review prevention with warning message

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

Product Management (Staff & Superusers Only):
- Add new products with variations directly from the frontend
- Edit existing products and variations from the frontend
- Delete products directly from the frontend
- Product management accessible without using the Django admin panel

---

## Custom Python Logic

The following custom Python logic has been implemented throughout the application to demonstrate Python proficiency and meet functional requirements:

| Location | Logic | Purpose |
|----------|-------|---------|
| `bag/contexts.py` | Dynamic delivery calculation | Delivery charge is automatically applied if the order total is below `FREE_DELIVERY_THRESHOLD`, otherwise delivery is free (£0) |
| `bag/contexts.py` | Grand total calculation | Grand total is dynamically calculated by combining order total and delivery cost |
| `bag/views.py` | Variation key generation | Unique keys are dynamically created from product variation combinations for session storage |
| `bag/views.py` | Quantity limit enforcement | Minimum quantity of 1 and maximum of 99 enforced per item in the bag |
| `bag/views.py` | Session bag management | Bag data stored and managed in Django session with full CRUD operations |
| `checkout/views.py` | Stripe PaymentIntent creation | Dynamic total sent to Stripe API in pence/cents for secure payment processing |
| `checkout/views.py` | Order line item creation | Order items programmatically saved from session bag data to database |
| `checkout/views.py` | Profile auto-fill | Checkout form pre-filled with saved profile data for authenticated users |
| `product/views.py` | Product filtering & sorting | Products dynamically filtered by category, search query, price, and rating |
| `product/views.py` | Variation grouping | Product variations grouped by type using Python's itertools groupby function |

---

## Database Schema

The schema below outlines all models and their relationships across the application.

![Database Schema](/static/screenshots/db_schema.png)

---

**1. Website Settings**

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

**2. Products**

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

Review
- id (PK)
- product: FK → Product
- user: FK → User
- rating: Integer (1-5)
- comment: Text
- is_active: Boolean
- created_at: DateTime
- updated_at: DateTime

**3. Orders**

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

**4. User Profiles**

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

**5. Sliders**

HeroSlider
- id (PK)
- title: Char(100)
- subtitle: Char(200)
- image: Image
- link: URLField

---

## Relationships

- Product → Brand: Many-to-One
- Product → Category: Many-to-One
- Product → Tag: Many-to-Many
- Product → ProductVariation: One-to-Many
- ProductVariation → Variation: Many-to-One
- Order → OrderLineItem: One-to-Many
- Order → UserProfile: Many-to-One
- User → UserProfile: One-to-One
- Category → Category: Self-referencing (parent category)
- Review → Product: Many-to-One
- Review → User: Many-to-One

---

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
| Product Details (Reviews) | Customer reviews, submit/edit/delete review | ![Reviews Desktop](/static/screenshots/reviews.png) | ![Reviews Tablet](/static/screenshots/reviews_tablet.png) | ![Reviews Mobile](/static/screenshots/reviews_mobile.png) |
| Add Product (Staff) | Add product form with variations inline | ![Add Product Desktop](/static/screenshots/add_product.png) | ![Add Product Tablet](/static/screenshots/add_product_tablet.png) | ![Add Product Mobile](/static/screenshots/add_product_mobile.png) |
| Edit Product (Staff) | Edit product form with existing data | ![Edit Product Desktop](/static/screenshots/edit_product.png) | ![Edit Product Tablet](/static/screenshots/edit_product_tablet.png) | ![Edit Product Mobile](/static/screenshots/edit_product_mobile.png) |


## User Stories

| Role | Action | Outcome |
|------|---------|----------|
| Visitor | Browse products by category | Find desired products easily |
| Visitor | Filter/sort products | View products by price, rating, or name |
| User | Add products to cart | Review selections and proceed to purchase |
| User | Checkout using Stripe | Secure and verified payment |
| User | Submit a product review | Share feedback on purchased products |
| User | Edit or delete own review | Manage personal review content |
| User | Manage profile | Update info and view past orders |
| Staff | Add or edit products from frontend | Manage shop content without admin panel |
| Staff | Delete products from frontend | Remove outdated or discontinued products |
| Admin | Manage products, categories, and orders | Maintain full control of shop content |


## Features

| SECTION             | DESCRIPTION                                                                                                     | Screenshot / Image                                       |
|---------------------|-----------------------------------------------------------------------------------------------------------------|----------------------------------------------------------|
| Header              | Top bar with free shipping message (left) and contact number (right). Main header with logo (left), search bar (center), cart & user icons (right). Cart icon shows product count. | ![Header](/static/screenshots/header.png)               |
| User Authentication | Login, signup, and password reset handled via Django Allauth. Displays "My Account" if logged in or "Login / Sign up" otherwise. | ![Auth](/static/screenshots/auth.png)                   |
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
| Review List         | All submitted reviews displayed on the product detail page with username, star rating, date, and comment.       | ![Review List](/static/screenshots/review_list.png)     |
| Add Review          | Signed-in users can submit a review with a star rating and comment directly from the product detail page.       | ![Add Review](/static/screenshots/add_review.png)       |
| Edit Review         | Users can edit their own review via a modal popup pre-filled with their existing rating and comment.            | ![Edit Review](/static/screenshots/edit_review.png)     |
| Delete Review       | Users can delete their own review via a confirmation modal directly from the product detail page.               | ![Delete Review](/static/screenshots/delete_review.png) |
| Add Product (Staff) | Staff and superusers can add new products with variations directly from the frontend without using admin panel. | ![Add Product](/static/screenshots/add_product.png)     |
| Edit Product (Staff)| Staff and superusers can edit existing products and variations from the frontend.                               | ![Edit Product](/static/screenshots/edit_product.png)   |
| Delete Product (Staff)| Staff and superusers can delete products directly from the frontend.                                          | ![Delete Product](/static/screenshots/delete_product.png)|
| Admin Panel         | Django Admin for full CRUD control on products, brands, categories, and orders.                                  | ![Admin](/static/screenshots/admin.png)                 |

---

## CRUD Functionality

The application implements full CRUD (Create, Read, Update, Delete) functionality from the frontend without relying on the Django admin panel:

**Normal Users (Signed In):**
- Create: Submit a product review
- Read: View all products and reviews
- Update: Edit their own review
- Delete: Delete their own review

**Staff / Superusers:**
- Create: Add new products with variations via frontend form
- Read: View all products and orders
- Update: Edit existing products and variations via frontend form
- Delete: Delete products directly from the frontend

---

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
- HackMD – README / testing documentation
- dbdiagram.io – Database schema design

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
Won't Have: Discount coupons or referral system (planned for future release)

Testing
-------
All features were manually tested on desktop, tablet, and mobile for responsiveness and functionality.  
Stripe test mode was used for payment verification.  
User registration and login were validated through Django Allauth flows.  
Errors, test logs, and screenshots are documented separately in `TESTING.md`.

---

## Deployment on Heroku

This project is deployed on **Heroku**. The following steps were taken to successfully deploy the application.

### Prerequisites

Before deploying, ensure the following are in place:
- A [Heroku account](https://heroku.com)
- A [GitHub account](https://github.com) with the project repository
- A [Neon PostgreSQL](https://neon.tech) or other external database
- A [Cloudinary account](https://cloudinary.com) for media file storage
- A [Stripe account](https://stripe.com) for payment processing
- Python and pip installed locally

---

### Step 1 — Prepare the Project for Deployment

Before pushing to Heroku, the following files must be in place:

**`requirements.txt`** — Lists all Python dependencies:
```bash
pip freeze > requirements.txt
```

**`Procfile`** — Tells Heroku how to run the application. Create in the root directory:
```
web: gunicorn ecommerce.wsgi
```

**`runtime.txt`** — Specifies the Python version (optional but recommended):
```
python-3.12.0
```

**`settings.py`** — Ensure the following are configured:
```python
import os
import dj_database_url

DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = [host.strip() for host in os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')]

DATABASES = {
    'default': dj_database_url.parse(os.getenv('DATABASE_URL'))
    if os.getenv('DATABASE_URL')
    else {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**`.gitignore`** — Ensure sensitive files are never committed:
```
*.pyc
__pycache__/
.env
db.sqlite3
media/
```

---

### Step 2 — Create a Heroku Application

1. Log in to [heroku.com](https://heroku.com)
2. Click **New** → **Create new app**
3. Enter a unique app name (e.g. `pcshop-ff340fe41fef`)
4. Select **Europe** as the region
5. Click **Create app**

---

### Step 3 — Connect to GitHub

1. In the Heroku dashboard go to the **Deploy** tab
2. Under **Deployment method** select **GitHub**
3. Click **Connect to GitHub** and grant the necessary permissions
4. Search for your repository name and click **Connect**
5. Select the branch to deploy (e.g. `main`)

---

### Step 4 — Configure Environment Variables

In the Heroku dashboard go to **Settings** → **Config Vars** → **Reveal Config Vars** and add the following:

| Variable | Value | Purpose |
|----------|-------|---------|
| `SECRET_KEY` | Your Django secret key | Django security |
| `DATABASE_URL` | Your PostgreSQL connection string | Database connection |
| `CLOUDINARY_URL` | Your Cloudinary URL | Media file storage |
| `STRIPE_PUBLIC_KEY` | Your Stripe public key | Stripe frontend |
| `STRIPE_SECRET_KEY` | Your Stripe secret key | Stripe backend |
| `STRIPE_WH_SECRET` | Your Stripe webhook secret | Stripe webhooks |
| `EMAIL_HOST_USER` | Your email address | Order confirmation emails |
| `EMAIL_HOST_PASS` | Your email app password | Order confirmation emails |
| `DEBUG` | `False` | Disable debug in production |
| `ALLOWED_HOSTS` | `pcshop-ff340fe41fef.herokuapp.com` | Allowed hosts for Django |

> ⚠️ Never commit any of these values to GitHub. Always use environment variables for sensitive credentials.

---

### Step 5 — Set Up the Database

The project uses an external **Neon PostgreSQL** database provided by Code Institute. After setting `DATABASE_URL` in Config Vars:

1. In the Heroku dashboard go to the **More** menu → **Run console**
2. Run the following commands:
```bash
python manage.py migrate
python manage.py createsuperuser
```

---

### Step 6 — Deploy the Application

1. In the Heroku dashboard go to the **Deploy** tab
2. Scroll to **Manual deploy**
3. Select the `main` branch
4. Click **Deploy Branch**
5. Wait for the build to complete
6. Click **Open app** to view the live site

For automatic deploys on every push to `main`, enable **Automatic Deploys** on the same page.

---

### Step 7 — Verify Deployment

After deploying, verify the following:
- The site loads correctly at the Heroku URL
- Products and categories display correctly
- User registration and login work via Django Allauth
- Products can be added to cart and checkout works
- Stripe test payments complete successfully
- Order confirmation emails are received
- Staff/superuser can add, edit, and delete products from the frontend
- Media images load correctly via Cloudinary

---

### Challenges Faced During Deployment

#### 1. `Pipfile` / `Pipfile.lock` Conflict
- During development the project contained a `Pipfile` and `Pipfile.lock`
- These caused Heroku to fail during the build process as it attempted to use Pipenv instead of pip
- **Fix:** Removed both files and relied solely on `requirements.txt` for dependency management

#### 2. Uvicorn & Procfile Configuration
- `uvicorn` was installed as the ASGI server but did not start automatically on Heroku
- Heroku requires an explicit `Procfile` in the project root to define how the app should run
- A minor mistake in the `Procfile` initially prevented the app from starting
- **Fix:** Corrected the `Procfile` to use `gunicorn`:
```
web: gunicorn ecommerce.wsgi
```

#### 3. Dyno Sleep & Lost Media Files
- On the Basic plan, Heroku dynos sleep after inactivity
- Upon restarting, all locally stored media files are permanently lost because Heroku uses an ephemeral filesystem
- **Fix:** Integrated **Cloudinary** as external media storage
  - All uploaded images are stored on and served from Cloudinary
  - Images persist regardless of dyno restarts or sleeping

#### 4. Environment Variables
- Sensitive settings such as `SECRET_KEY`, `DATABASE_URL`, and API keys cannot be committed to a public repository
- **Fix:** All credentials configured securely via Heroku **Config Vars** — never stored in the codebase

#### 5. Static Files Not Loading
- After deployment, CSS and JavaScript files were not loading correctly
- **Fix:** Added `whitenoise` middleware to serve static files on Heroku:
```python
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    ...
]
```
And added to `settings.py`:
```python
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```
Then ran:
```bash
python manage.py collectstatic
```

#### 6. Database Migration on Remote
- After adding new models locally (e.g. the `Review` model), the remote database did not have the new tables
- Running the app on Heroku threw `ProgrammingError: relation does not exist`
- **Fix:** Always run migrations on Heroku after adding new models:
```bash
heroku run python manage.py migrate --app pcshop-ff340fe41fef
```

---

### Local Development

**Cloning the Repository:**

1. Go to the GitHub repository
2. Click the green **Code** button and copy the URL
3. Open Terminal or Git Bash and navigate to your project directory
4. Run:
```bash
git clone <repository-url>
cd <project-folder>
```

**Setting Up the Environment:**

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add:
```
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
STRIPE_PUBLIC_KEY=your_stripe_public_key
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_WH_SECRET=your_stripe_webhook_secret
EMAIL_HOST_USER=your_email
EMAIL_HOST_PASS=your_email_password
DEBUG=True
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

7. Visit `http://127.0.0.1:8000` in your browser

---

### Local vs Deployment

Minor differences may exist between the local and deployed versions due to environment settings, database connections, Cloudinary connections, `ALLOWED_HOSTS`, email settings, and API keys.

---

Future Features
---------------
- Dark mode toggle
- Wishlist/favorites
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