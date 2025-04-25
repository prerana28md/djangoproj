from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Pet, HealthRecord
from .forms import PetForm, HealthRecordForm

# Create your views here.

class PetListView(LoginRequiredMixin, ListView):
    model = Pet
    template_name = 'pets/pet_list.html'
    context_object_name = 'pets'

    def get_queryset(self):
        # Show all pets instead of filtering by owner
        pets = Pet.objects.all()
        print("\n=== Debug Information ===")
        print(f"Current user: {self.request.user.username}")
        print(f"Total pets in database: {pets.count()}")
        print("\nAll pets in database:")
        for pet in pets:
            print(f"- {pet.name} (ID: {pet.id}, Owner: {pet.owner.username})")
        print("=======================\n")
        return pets

class PetDetailView(LoginRequiredMixin, DetailView):
    model = Pet
    template_name = 'pets/pet_detail.html'
    context_object_name = 'pet'

    def get_queryset(self):
        # Show all pets instead of filtering by owner
        return Pet.objects.all()

class PetCreateView(LoginRequiredMixin, CreateView):
    model = Pet
    form_class = PetForm
    template_name = 'pets/pet_form.html'
    success_url = reverse_lazy('pets:pet_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class PetUpdateView(LoginRequiredMixin, UpdateView):
    model = Pet
    form_class = PetForm
    template_name = 'pets/pet_form.html'
    success_url = reverse_lazy('pets:pet_list')

    def get_queryset(self):
        # Only allow owners to update their pets
        return Pet.objects.filter(owner=self.request.user)

class PetDeleteView(LoginRequiredMixin, DeleteView):
    model = Pet
    template_name = 'pets/pet_confirm_delete.html'
    success_url = reverse_lazy('pets:pet_list')

    def get_queryset(self):
        # Only allow owners to delete their pets
        return Pet.objects.filter(owner=self.request.user)

class HealthRecordListView(LoginRequiredMixin, ListView):
    model = HealthRecord
    template_name = 'pets/health_record_list.html'
    context_object_name = 'health_records'

    def get_queryset(self):
        pet = get_object_or_404(Pet, pk=self.kwargs['pet_pk'])
        return HealthRecord.objects.filter(pet=pet)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pet'] = get_object_or_404(Pet, pk=self.kwargs['pet_pk'])
        return context

class HealthRecordCreateView(LoginRequiredMixin, CreateView):
    model = HealthRecord
    form_class = HealthRecordForm
    template_name = 'pets/health_record_form.html'

    def get_success_url(self):
        return reverse_lazy('pets:health_record_list', kwargs={'pet_pk': self.kwargs['pet_pk']})

    def form_valid(self, form):
        pet = get_object_or_404(Pet, pk=self.kwargs['pet_pk'])
        form.instance.pet = pet
        return super().form_valid(form)
