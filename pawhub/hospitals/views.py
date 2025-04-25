from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Hospital

# Create your views here.

class HospitalListView(ListView):
    model = Hospital
    template_name = 'hospitals/hospital_list.html'
    context_object_name = 'hospitals'

class HospitalDetailView(DetailView):
    model = Hospital
    template_name = 'hospitals/hospital_detail.html'
    context_object_name = 'hospital'

class HospitalCreateView(LoginRequiredMixin, CreateView):
    model = Hospital
    template_name = 'hospitals/hospital_form.html'
    fields = ['name', 'address', 'contact', 'email', 'website', 'description', 'image']
    success_url = reverse_lazy('hospitals:list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add New Hospital'
        return context

class HospitalUpdateView(LoginRequiredMixin, UpdateView):
    model = Hospital
    template_name = 'hospitals/hospital_form.html'
    fields = ['name', 'address', 'contact', 'email', 'website', 'description', 'image']
    success_url = reverse_lazy('hospitals:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Hospital'
        return context

class HospitalDeleteView(LoginRequiredMixin, DeleteView):
    model = Hospital
    template_name = 'hospitals/hospital_confirm_delete.html'
    success_url = reverse_lazy('hospitals:list')
