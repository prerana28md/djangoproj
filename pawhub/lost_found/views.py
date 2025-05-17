from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import LostFound
from .forms import LostPetForm, FoundPetForm
from django.db.models import Q

# Create your views here.

class LostFoundListView(ListView):
    model = LostFound
    template_name = 'lost_found/lostfound_list.html'
    context_object_name = 'items'
    paginate_by = 12

    def get_queryset(self):
        queryset = LostFound.objects.all()
        search_query = self.request.GET.get('search', '')
        status = self.request.GET.get('status', '')
        date = self.request.GET.get('date', '')

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(location__icontains=search_query)
            )

        if status:
            queryset = queryset.filter(status=status)

        if date:
            queryset = queryset.filter(date=date)

        return queryset.order_by('-created_at')

class LostFoundDetailView(DetailView):
    model = LostFound
    template_name = 'lost_found/lostfound_detail.html'
    context_object_name = 'item'

class LostFoundCreateView(LoginRequiredMixin, CreateView):
    model = LostFound
    template_name = 'lost_found/lostfound_form.html'
    success_url = reverse_lazy('lost_found:list')

    def get_form_class(self):
        status = self.request.GET.get('status', 'lost')
        return LostPetForm if status == 'lost' else FoundPetForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class LostFoundUpdateView(LoginRequiredMixin, UpdateView):
    model = LostFound
    template_name = 'lost_found/lostfound_form.html'
    success_url = reverse_lazy('lost_found:list')

    def get_form_class(self):
        return LostPetForm if self.object.status == 'lost' else FoundPetForm

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

class LostFoundDeleteView(LoginRequiredMixin, DeleteView):
    model = LostFound
    template_name = 'lost_found/lostfound_confirm_delete.html'
    success_url = reverse_lazy('lost_found:list')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
