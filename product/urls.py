from django.urls import path
from product import views

urlpatterns = [
    path('', views.all_products, name='all_products'),
    path(
        "category/<slug:category_slug>/",
        views.all_products,
        name="category"
    ),
    path('<slug:product_slug>/', views.product_detail, name='product_detail'),
    # Review
    path(
        'review/<int:review_id>/edit/',
        views.edit_review,
        name='edit_review'
    ),
    path(
        'review/<int:review_id>/delete/',
        views.delete_review,
        name='delete_review'
    ),
    # Product CRUD
    path('product/add/', views.add_product, name='add_product'),
    path(
        'product/<slug:product_slug>/edit/',
        views.edit_product,
        name='edit_product'
    ),
    path(
        'product/<slug:product_slug>/delete/',
        views.delete_product,
        name='delete_product'
    ),
]