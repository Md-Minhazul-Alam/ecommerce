from django.urls import path
from product import views

urlpatterns = [
    path('', views.all_products, name='all_products'),
    # path('<product_id>', views.product_detail, name='product_detail'),
    path('/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path("/category/<slug:category_slug>/", views.all_products, name="category"),


]