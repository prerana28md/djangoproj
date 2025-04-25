from django.urls import path
from . import views

app_name = 'hospitals'

urlpatterns = [
    path('', views.HospitalListView.as_view(), name='list'),
    path('create/', views.HospitalCreateView.as_view(), name='create'),
    path('<int:pk>/', views.HospitalDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.HospitalUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.HospitalDeleteView.as_view(), name='delete'),
    
    # Doctor URLs
    path('<int:hospital_pk>/doctors/create/', views.doctor_create, name='doctor_create'),
    path('doctors/<int:pk>/update/', views.doctor_update, name='doctor_update'),
    path('doctors/<int:pk>/delete/', views.doctor_delete, name='doctor_delete'),
] 