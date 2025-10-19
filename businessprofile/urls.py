from django.urls import path
from businessprofile import views

urlpatterns = [
    path('quick-link/<slug:slug>/', views.quick_link_detail, name='quick_link_detail'),
    path('legal/<slug:slug>/', views.legal_link_detail, name='legal_link_detail'),
]