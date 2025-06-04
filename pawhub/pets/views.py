from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Pet, HealthRecord
from .forms import PetForm, HealthRecordForm

# Create your views here.

def pet_list(request):
    pets = Pet.objects.all()
    search_query = request.GET.get('search', '')
    pet_type = request.GET.get('species', '')
    type = request.GET.get('type', '')
    age_range = request.GET.get('age_range', '')
    status = request.GET.get('status', '')
    
    if search_query:
        pets = pets.filter(
            Q(name__icontains=search_query) |
            Q(breed__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    if pet_type:
        pets = pets.filter(species=pet_type)
    
    if type:
        pets = pets.filter(type=type)
    
    if status:
        pets = pets.filter(status=status)
    
    if age_range:
        if age_range == '0-1':
            pets = pets.filter(age__gte=0, age__lt=1)
        elif age_range == '1-3':
            pets = pets.filter(age__gte=1, age__lt=3)
        elif age_range == '3-5':
            pets = pets.filter(age__gte=3, age__lt=5)
        elif age_range == '5+':
            pets = pets.filter(age__gte=5)
    
    pets = pets.order_by('-created_at')
    
    paginator = Paginator(pets, 12)  # Show 12 pets per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'pets': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
        'types': Pet.TYPE_CHOICES,
        'statuses': Pet.STATUS_CHOICES,
        'species': Pet.SPECIES_CHOICES,
    }
    
    return render(request, 'pets/pet_list.html', context)

@login_required
def pet_create(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.save()
            messages.success(request, f'Pet added successfully and listed for {pet.get_type_display()}!')
            return redirect('pets:pet_list')
    else:
        form = PetForm()
    return render(request, 'pets/pet_form.html', {'form': form})

@login_required
def pet_detail(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    health_records = pet.health_records.all().order_by('-date')
    return render(request, 'pets/pet_detail.html', {
        'pet': pet,
        'health_records': health_records
    })

@login_required
def pet_update(request, pk):
    pet = get_object_or_404(Pet, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pet updated successfully!')
            return redirect('pets:pet_detail', pk=pet.pk)
    else:
        form = PetForm(instance=pet)
    return render(request, 'pets/pet_form.html', {'form': form})

@login_required
def pet_delete(request, pk):
    pet = get_object_or_404(Pet, pk=pk, owner=request.user)
    if request.method == 'POST':
        pet.delete()
        messages.success(request, 'Pet deleted successfully!')
        return redirect('pets:pet_list')
    return render(request, 'pets/pet_confirm_delete.html', {'pet': pet})

@login_required
def health_record_create(request, pet_pk):
    pet = get_object_or_404(Pet, pk=pet_pk, owner=request.user)
    if request.method == 'POST':
        form = HealthRecordForm(request.POST, request.FILES)
        if form.is_valid():
            health_record = form.save(commit=False)
            health_record.pet = pet
            health_record.save()
            messages.success(request, 'Health record added successfully!')
            return redirect('pets:pet_detail', pk=pet.pk)
    else:
        form = HealthRecordForm()
    return render(request, 'pets/health_record_form.html', {'form': form, 'pet': pet})

class PetListView(ListView):
    model = Pet
    template_name = 'pets/pet_list.html'
    context_object_name = 'pets'
    paginate_by = 12

    def get_queryset(self):
        queryset = Pet.objects.select_related('owner').all()
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(breed__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(location__icontains=search_query)
            )
        
        # Filter by type
        pet_type = self.request.GET.get('type')
        if pet_type:
            queryset = queryset.filter(type=pet_type)
        
        # Filter by species
        species = self.request.GET.get('species')
        if species:
            queryset = queryset.filter(species=species)
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by age range
        age_range = self.request.GET.get('age_range')
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'types': Pet.TYPE_CHOICES,
            'statuses': Pet.STATUS_CHOICES,
            'species': Pet.SPECIES_CHOICES,
        })
        return context

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

@login_required
def mark_pet_lost(request, pk):
    pet = get_object_or_404(Pet, pk=pk, owner=request.user)
    pet.type = 'lost'
    pet.save()
    messages.success(request, f"{pet.name} has been marked as lost.")
    return redirect('pets:my_lost_pets')

@login_required
def mark_pet_found(request, pk):
    pet = get_object_or_404(Pet, pk=pk, owner=request.user)
    pet.type = 'found'
    pet.save()
    messages.success(request, f"{pet.name} has been marked as found.")
    return redirect('pets:my_lost_pets')

@login_required
def my_lost_pets(request):
    lost_pets = Pet.objects.filter(owner=request.user, type='lost').order_by('-created_at')
    return render(request, 'pets/my_lost_pets.html', {'lost_pets': lost_pets})
