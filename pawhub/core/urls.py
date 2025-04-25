from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('profile/', views.profile_view, name='profile'),
    path('pets/', views.pet_list, name='pet_list'),
    path('pets/create/', views.pet_create, name='pet_create'),
    path('pets/<int:pk>/', views.pet_detail, name='pet_detail'),
    path('pets/<int:pk>/update/', views.pet_update, name='pet_update'),
    path('pets/<int:pk>/delete/', views.pet_delete, name='pet_delete'),
    path('listings/', views.listing_list, name='listing_list'),
    path('listings/create/', views.listing_create, name='listing_create'),
    path('listings/<int:pk>/', views.listing_detail, name='listing_detail'),
    path('listings/<int:pk>/update/', views.listing_update, name='listing_update'),
    path('listings/<int:pk>/delete/', views.listing_delete, name='listing_delete'),
    path('browse/', views.public_listings, name='public_listings'),  # optional public view
    path('marketplace/', views.marketplace, name='marketplace'),
    path('marketplace/create/', views.marketplace_item_create, name='marketplace_item_create'),
    path('marketplace/<int:pk>/', views.marketplace_item_detail, name='marketplace_item_detail'),
    path('marketplace/<int:pk>/update/', views.marketplace_item_update, name='marketplace_item_update'),
    path('marketplace/<int:pk>/delete/', views.marketplace_item_delete, name='marketplace_item_delete'),
    path('lost-found/', views.lost_found, name='lost_found'),
]
