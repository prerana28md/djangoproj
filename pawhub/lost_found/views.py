from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import LostFound

# Create your views here.

class LostFoundListView(ListView):
    model = LostFound
    template_name = 'lost_found/lostfound_list.html'
    context_object_name = 'items'

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
