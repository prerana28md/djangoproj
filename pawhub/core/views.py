from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Pet, Listing, HealthRecord, MarketplaceItem
from .forms import PetForm, ListingForm, HealthRecordForm, MarketplaceItemForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.db.models import Q
from users.forms import UserRegistrationForm

# ----------------------
# 🐶 Pet Views
# ----------------------

@login_required
def pet_list(request):
    pets = Pet.objects.all()  # Show all pets instead of filtering by owner
    return render(request, 'core/pet_list.html', {'pets': pets})

@login_required
def pet_create(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.save()
            messages.success(request, 'Pet added successfully!')
            return redirect('core:pet_list')
    else:
        form = PetForm()
    return render(request, 'core/pet_form.html', {'form': form})

@login_required
def pet_detail(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    if request.method == 'POST' and request.user == pet.owner:
        health_status = request.POST.get('health_status')
        vaccination_status = request.POST.get('vaccination_status')
        if health_status:
            pet.health_status = health_status
        if vaccination_status:
            pet.vaccination_status = vaccination_status
        pet.save()
        messages.success(request, 'Pet information updated successfully!')
        return redirect('core:pet_detail', pk=pk)
    return render(request, 'core/pet_detail.html', {'pet': pet})

@login_required
def pet_update(request, pk):
    pet = get_object_or_404(Pet, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pet updated successfully!')
            return redirect('core:pet_detail', pk=pet.pk)
    else:
        form = PetForm(instance=pet)
    return render(request, 'core/pet_form.html', {'form': form})

@login_required
def pet_delete(request, pk):
    pet = get_object_or_404(Pet, pk=pk, owner=request.user)
    if request.method == 'POST':
        pet.delete()
        messages.success(request, 'Pet deleted successfully!')
        return redirect('core:pet_list')
    return render(request, 'core/pet_confirm_delete.html', {'pet': pet})

# ----------------------
# 📋 Listing Views
# ----------------------

@login_required
def listing_list(request):
    listings = Listing.objects.filter(pet__owner=request.user)
    return render(request, 'core/listing_list.html', {'listings': listings})

@login_required
def listing_create(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.pet = form.cleaned_data['pet']
            listing.save()
            messages.success(request, 'Listing created successfully!')
            return redirect('core:listing_list')
    else:
        form = ListingForm(user=request.user)
    return render(request, 'core/listing_form.html', {'form': form})

@login_required
def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk, pet__owner=request.user)
    return render(request, 'core/listing_detail.html', {'listing': listing})

@login_required
def listing_update(request, pk):
    listing = get_object_or_404(Listing, pk=pk, pet__owner=request.user)
    if request.method == 'POST':
        form = ListingForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            messages.success(request, 'Listing updated successfully!')
            return redirect('core:listing_detail', pk=listing.pk)
    else:
        form = ListingForm(instance=listing, user=request.user)
    return render(request, 'core/listing_form.html', {'form': form})

@login_required
def listing_delete(request, pk):
    listing = get_object_or_404(Listing, pk=pk, pet__owner=request.user)
    if request.method == 'POST':
        listing.delete()
        messages.success(request, 'Listing deleted successfully!')
        return redirect('core:listing_list')
    return render(request, 'core/listing_confirm_delete.html', {'listing': listing})

def public_listings(request):
    listings = Listing.objects.filter(status='available')
    return render(request, 'core/public_listings.html', {'listings': listings})

def home(request):
    return render(request, 'core/home.html')

# ----------------------
# 🛍️ Marketplace Views
# ----------------------

@login_required
def marketplace(request):
    items = MarketplaceItem.objects.all()
    return render(request, 'core/marketplace.html', {'items': items})

@login_required
def marketplace_item_create(request):
    if request.method == 'POST':
        form = MarketplaceItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.seller = request.user
            item.save()
            messages.success(request, 'Item added successfully!')
            return redirect('core:marketplace')
    else:
        form = MarketplaceItemForm()
    return render(request, 'core/marketplace_item_form.html', {'form': form, 'title': 'Add New Item'})

@login_required
def marketplace_item_detail(request, pk):
    item = get_object_or_404(MarketplaceItem, pk=pk)
    return render(request, 'core/marketplace_item_detail.html', {'item': item})

@login_required
def marketplace_item_update(request, pk):
    item = get_object_or_404(MarketplaceItem, pk=pk, seller=request.user)
    if request.method == 'POST':
        form = MarketplaceItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item updated successfully!')
            return redirect('core:marketplace_item_detail', pk=item.pk)
    else:
        form = MarketplaceItemForm(instance=item)
    return render(request, 'core/marketplace_item_form.html', {'form': form, 'title': 'Edit Item'})

@login_required
def marketplace_item_delete(request, pk):
    item = get_object_or_404(MarketplaceItem, pk=pk, seller=request.user)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item deleted successfully!')
        return redirect('core:marketplace')
    return render(request, 'core/marketplace_item_confirm_delete.html', {'item': item})

def lost_found(request):
    return render(request, 'core/lost_found.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('core:home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('core:home')

class SignUpView(CreateView):
    form_class = UserRegistrationForm
    success_url = reverse_lazy('core:login')
    template_name = 'core/signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Account created successfully! Please log in.')
        return response

@login_required
def profile_view(request):
    return render(request, 'core/profile.html')
