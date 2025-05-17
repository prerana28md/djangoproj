from django.urls import path
from . import views

app_name = 'marketplace'

urlpatterns = [
    # Marketplace Items
    path('', views.marketplace_item_list, name='marketplace_item_list'),
    path('item/create/', views.marketplace_item_create, name='marketplace_item_create'),
    path('item/<int:pk>/', views.marketplace_item_detail, name='marketplace_item_detail'),
    path('item/<int:pk>/update/', views.marketplace_item_update, name='marketplace_item_update'),
    path('item/<int:pk>/delete/', views.marketplace_item_delete, name='marketplace_item_delete'),
    
    # Pet Listings
    path('pets/', views.pet_listing_list, name='pet_listing_list'),
    path('pets/create/', views.pet_listing_create, name='pet_listing_create'),
    path('pets/<int:pk>/', views.pet_listing_detail, name='pet_listing_detail'),
    
    # Cart Management
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    
    # Shop Management
    path('shop/dashboard/', views.shop_dashboard, name='shop_dashboard'),
    path('shop/orders/', views.shop_orders, name='shop_orders'),
    path('shop/orders/<int:pk>/', views.shop_order_detail, name='shop_order_detail'),
] 