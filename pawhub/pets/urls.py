from django.urls import path
from . import views

app_name = 'pets'

urlpatterns = [
    path('', views.PetListView.as_view(), name='pet_list'),
    path('create/', views.PetCreateView.as_view(), name='pet_create'),
    path('<int:pk>/', views.PetDetailView.as_view(), name='pet_detail'),
    path('<int:pk>/update/', views.PetUpdateView.as_view(), name='pet_update'),
    path('<int:pk>/delete/', views.PetDeleteView.as_view(), name='pet_delete'),
    path('<int:pet_pk>/health-records/', views.HealthRecordListView.as_view(), name='health_record_list'),
    path('<int:pet_pk>/health-records/create/', views.HealthRecordCreateView.as_view(), name='health_record_create'),
] 