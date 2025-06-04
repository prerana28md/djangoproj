from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Home and Authentication
    path('', views.home, name='home'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout_view'),
    
    # Pet Management
    path('pets/', views.pet_list, name='pet_list'),
    path('pets/create/', views.pet_create, name='pet_create'),
    path('pets/<int:pk>/', views.pet_detail, name='pet_detail'),
    path('pets/<int:pk>/update/', views.pet_update, name='pet_update'),
    path('pets/<int:pk>/delete/', views.pet_delete, name='pet_delete'),
    path('pets/<int:pk>/mark-found/', views.mark_pet_found, name='mark_pet_found'),
    path('pets/<int:pk>/mark-lost/', views.mark_pet_lost, name='mark_pet_lost'),
    
    # Adoption and Exchange
    path('pets/<int:pet_pk>/adopt/', views.adoption_request_create, name='adoption_request_create'),
    path('pets/<int:pet_pk>/exchange/', views.exchange_request_create, name='exchange_request_create'),
    path('adoption-requests/', views.adoption_request_list, name='adoption_request_list'),
    path('adoption-requests/<int:pk>/response/', views.adoption_request_response, name='adoption_request_response'),
    
    # Listings
    path('listings/', views.listing_list, name='listing_list'),
    path('listings/create/', views.listing_create, name='listing_create'),
    path('listings/<int:pk>/', views.listing_detail, name='listing_detail'),
    path('listings/<int:pk>/update/', views.listing_update, name='listing_update'),
    path('listings/<int:pk>/delete/', views.listing_delete, name='listing_delete'),
    path('browse/', views.public_listings, name='public_listings'),
    
    # Marketplace
    path('marketplace/', views.marketplace_list, name='marketplace_list'),
    path('marketplace/item/create/', views.marketplace_item_create, name='marketplace_item_create'),
    path('marketplace/item/<int:pk>/', views.marketplace_item_detail, name='marketplace_item_detail'),
    path('marketplace/item/<int:pk>/update/', views.marketplace_item_update, name='marketplace_item_update'),
    path('marketplace/item/<int:pk>/delete/', views.marketplace_item_delete, name='marketplace_item_delete'),
    path('marketplace/dashboard/', views.shop_owner_dashboard, name='shop_owner_dashboard'),
    
    # Cart and Orders
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:item_pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
    path('orders/<int:pk>/cancel/', views.order_cancel, name='order_cancel'),
    
    # Lost and Found
    path('lost-found/', views.lost_found, name='lost_found'),
    
    # Login and Signup
    path('login/', views.login_view, name='login'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
]
