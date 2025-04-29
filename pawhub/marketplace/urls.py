from django.urls import path
from . import views

app_name = 'marketplace'

urlpatterns = [
    path('', views.marketplace_item_list, name='list'),
    path('create/', views.marketplace_item_create, name='create'),
    path('<int:pk>/', views.marketplace_item_detail, name='detail'),
    path('<int:pk>/update/', views.marketplace_item_update, name='update'),
    path('<int:pk>/delete/', views.marketplace_item_delete, name='delete'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    # Pet listing URLs
    path('pets/', views.pet_listing_list, name='pet_listing_list'),
    path('pets/create/', views.pet_listing_create, name='pet_listing_create'),
    path('pets/<int:pk>/', views.pet_listing_detail, name='pet_listing_detail'),
    path('pets/<int:pk>/purchase/', views.pet_listing_purchase, name='pet_listing_purchase'),
] 