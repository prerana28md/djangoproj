from django.urls import path
from . import views

app_name = 'lost_found'

urlpatterns = [
    path('', views.LostFoundListView.as_view(), name='list'),
    path('create/', views.LostFoundCreateView.as_view(), name='create'),
    path('<int:pk>/', views.LostFoundDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.LostFoundUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.LostFoundDeleteView.as_view(), name='delete'),
] 