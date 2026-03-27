from django.urls import path
from product import views

urlpatterns = [
    path('', views.all_products, name='all_products'),
    path("category/<slug:category_slug>/", views.all_products, name="category"),
    path('<slug:product_slug>/', views.product_detail, name='product_detail'),
    # Review
    path('review/<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
]