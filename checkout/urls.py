from django.urls import path
from checkout import views
from .import webhook

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('checkout_success/<order_number>', views.checkout_success, name='checkout_success'),
    path('webhook/', webhook.webhook, name='stripe_webhook'),
    path('cache_checkout_data/', views.cache_checkout_data, name='cache_checkout_data'),
]