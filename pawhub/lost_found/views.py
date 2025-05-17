from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import LostFound
from core.models import Pet
from django.db.models import Q

# Create your views here.

class LostFoundListView(ListView):
    model = Pet
    template_name = 'lost_found/lostfound_list.html'
    context_object_name = 'pets'
    paginate_by = 12

    def get_queryset(self):
        queryset = Pet.objects.filter(adoption_status='available')
        search_query = self.request.GET.get('search', '')
        pet_type = self.request.GET.get('species', '')
        age_range = self.request.GET.get('age_range', '')

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(breed__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        if pet_type:
            queryset = queryset.filter(type=pet_type)

        if age_range:
            if age_range == '0-1':
                queryset = queryset.filter(age__gte=0, age__lt=1)
            elif age_range == '1-3':
                queryset = queryset.filter(age__gte=1, age__lt=3)
            elif age_range == '3-5':
                queryset = queryset.filter(age__gte=3, age__lt=5)
            elif age_range == '5+':
                queryset = queryset.filter(age__gte=5)

        return queryset.order_by('-created_at')

class LostFoundDetailView(DetailView):
    model = LostFound
    template_name = 'lost_found/lostfound_detail.html'
    context_object_name = 'item'

class LostFoundCreateView(LoginRequiredMixin, CreateView):
    model = LostFound
    template_name = 'lost_found/lostfound_form.html'
    fields = ['title', 'description', 'status', 'location', 'date', 'image', 'contact_info']
    success_url = reverse_lazy('lost_found:list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class LostFoundUpdateView(LoginRequiredMixin, UpdateView):
    model = LostFound
    template_name = 'lost_found/lostfound_form.html'
    fields = ['title', 'description', 'status', 'location', 'date', 'image', 'contact_info']
    success_url = reverse_lazy('lost_found:list')

class LostFoundDeleteView(LoginRequiredMixin, DeleteView):
    model = LostFound
    template_name = 'lost_found/lostfound_confirm_delete.html'
    success_url = reverse_lazy('lost_found:list')
