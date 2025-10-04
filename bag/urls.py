from django.urls import path
from bag import views

urlpatterns = [
    path('', views.view_bag, name='view_bag'),
    path('add/<item_id>/', views.add_to_bag, name='add_to_bag'),
    path('remove/<item_id>/', views.remove_from_bag, name='remove_from_bag'),
    path('increment/<item_id>/', views.increment_bag_item, name='increment_bag_item'),
    path('decrement/<item_id>/', views.decrement_bag_item, name='decrement_bag_item'),
]