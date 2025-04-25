from django.urls import path
from . import views

app_name = 'hospitals'

urlpatterns = [
    path('', views.HospitalListView.as_view(), name='list'),
    path('create/', views.HospitalCreateView.as_view(), name='create'),
    path('<int:pk>/', views.HospitalDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.HospitalUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.HospitalDeleteView.as_view(), name='delete'),
] 