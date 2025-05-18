from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils import timezone
from .models import Pet, Listing, HealthRecord, MarketplaceItem, AdoptionRequest, Cart, CartItem, Order, OrderItem
from lost_found.models import LostFound
from .forms import PetForm, ListingForm, HealthRecordForm, MarketplaceItemForm, AdoptionRequestForm, AdoptionRequestResponseForm, CartItemForm, OrderForm, MarketplaceSearchForm
from lost_found.forms import LostPetForm, FoundPetForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from users.forms import UserRegistrationForm
from django.http import JsonResponse

# ----------------------
# 🐶 Pet Views
# ----------------------

@login_required
def pet_create(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.save()
            
            # Create a listing for the pet
            listing = Listing.objects.create(
                pet=pet,
                listing_type='adoption',  # Default to adoption
                status='available'
            )
            
            messages.success(request, 'Pet added successfully and listed for adoption!')
            return redirect('core:pet_list')
    else:
        form = PetForm()
    return render(request, 'core/pet_form.html', {'form': form})

@login_required
def pet_detail(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    # Get the most recent active listing for the pet
    listing = Listing.objects.filter(pet=pet, status='available').order_by('-date_posted').first()
    if not listing:
        listing = Listing.objects.filter(pet=pet).order_by('-date_posted').first()
    
    adoption_request = None
    health_records = pet.healthrecord_set.all().order_by('-record_date')
    
    if request.user != pet.owner:
        adoption_request = AdoptionRequest.objects.filter(pet=pet, requester=request.user).first()
    
    return render(request, 'core/pet_detail.html', {
        'pet': pet,
        'listing': listing,
        'adoption_request': adoption_request,
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
    listing_type = request.GET.get('type', '')
    search_query = request.GET.get('search', '')
    pet_type = request.GET.get('species', '')
    age_range = request.GET.get('age_range', '')
    
    if listing_type:
        listings = listings.filter(listing_type=listing_type)
    
    if search_query:
        listings = listings.filter(
            Q(pet__name__icontains=search_query) |
            Q(pet__breed__icontains=search_query) |
            Q(pet__description__icontains=search_query)
        )
    
    if pet_type:
        listings = listings.filter(pet__type=pet_type)
    
    if age_range:
        if age_range == '0-1':
            listings = listings.filter(pet__age__gte=0, pet__age__lt=1)
        elif age_range == '1-3':
            listings = listings.filter(pet__age__gte=1, pet__age__lt=3)
        elif age_range == '3-5':
            listings = listings.filter(pet__age__gte=3, pet__age__lt=5)
        elif age_range == '5+':
            listings = listings.filter(pet__age__gte=5)
    
    listings = listings.order_by('-date_posted')
    
    paginator = Paginator(listings, 12)  # Show 12 listings per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'core/public_listings.html', {
        'listings': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
        'current_type': listing_type
    })

def home(request):
    return render(request, 'core/home.html')

def pet_list(request):
    pets = Pet.objects.all()
    search_query = request.GET.get('search', '')
    pet_type = request.GET.get('species', '')  # Keep the parameter name as 'species' for backward compatibility
    age_range = request.GET.get('age_range', '')
    
    if search_query:
        pets = pets.filter(
            Q(name__icontains=search_query) |
            Q(breed__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    if pet_type:
        pets = pets.filter(type=pet_type)
    
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
    
    return render(request, 'core/pet_list.html', {
        'pets': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj
    })

# ----------------------
# 🛍️ Marketplace Views
# ----------------------

@login_required
def marketplace_list(request):
    form = MarketplaceSearchForm(request.GET)
    items = MarketplaceItem.objects.all()
    
    if form.is_valid():
        category = form.cleaned_data.get('category')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        search = form.cleaned_data.get('search')
        
        if category:
            items = items.filter(category=category)
        if min_price:
            items = items.filter(price__gte=min_price)
        if max_price:
            items = items.filter(price__lte=max_price)
        if search:
            items = items.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )
    
    return render(request, 'core/marketplace_list.html', {
        'items': items,
        'form': form
    })

@login_required
def marketplace_item_create(request):
    if request.method == 'POST':
        form = MarketplaceItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.shop_owner = request.user
            item.save()
            messages.success(request, 'Item added successfully!')
            return redirect('core:marketplace_list')
    else:
        form = MarketplaceItemForm()
    
    return render(request, 'core/marketplace_item_form.html', {'form': form})

@login_required
def marketplace_item_detail(request, pk):
    item = get_object_or_404(MarketplaceItem, pk=pk, shop_owner=request.user)
    return render(request, 'core/marketplace_item_detail.html', {'item': item})

@login_required
def marketplace_item_update(request, pk):
    item = get_object_or_404(MarketplaceItem, pk=pk, shop_owner=request.user)
    if request.user != item.shop_owner:
        messages.error(request, 'You do not have permission to edit this item.')
        return redirect('core:marketplace_list')
    
    if request.method == 'POST':
        form = MarketplaceItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item updated successfully!')
            return redirect('core:marketplace_list')
    else:
        form = MarketplaceItemForm(instance=item)
    
    return render(request, 'core/marketplace_item_form.html', {'form': form})

@login_required
def marketplace_item_delete(request, pk):
    item = get_object_or_404(MarketplaceItem, pk=pk, shop_owner=request.user)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item deleted successfully!')
        return redirect('core:marketplace_list')
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
    success_url = reverse_lazy('users:login')
    template_name = 'core/signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Account created successfully! Please log in.')
        return response

@login_required
def profile_view(request):
    return render(request, 'core/profile.html')

# Adoption Request Views
@login_required
def adoption_request_create(request, pet_pk):
    pet = get_object_or_404(Pet, pk=pet_pk)
    if request.user == pet.owner:
        messages.error(request, 'You cannot request to adopt your own pet.')
        return redirect('core:pet_detail', pk=pet_pk)
    
    if request.method == 'POST':
        form = AdoptionRequestForm(request.POST)
        if form.is_valid():
            adoption_request = form.save(commit=False)
            adoption_request.pet = pet
            adoption_request.requester = request.user
            adoption_request.save()
            
            # Update pet status
            pet.adoption_status = 'requested'
            pet.save()
            
            messages.success(request, 'Adoption request submitted successfully!')
            return redirect('core:pet_detail', pk=pet_pk)
    else:
        form = AdoptionRequestForm()
    
    return render(request, 'core/adoption_request_form.html', {
        'form': form,
        'pet': pet
    })

@login_required
def exchange_request_create(request, pet_pk):
    pet = get_object_or_404(Pet, pk=pet_pk)
    if request.user == pet.owner:
        messages.error(request, 'You cannot request to exchange your own pet.')
        return redirect('core:pet_detail', pk=pet_pk)
    
    if request.method == 'POST':
        form = AdoptionRequestForm(request.POST)  # Reusing adoption request form for now
        if form.is_valid():
            exchange_request = form.save(commit=False)
            exchange_request.pet = pet
            exchange_request.requester = request.user
            exchange_request.request_type = 'exchange'  # Mark as exchange request
            exchange_request.save()
            
            messages.success(request, 'Exchange request submitted successfully!')
            return redirect('core:pet_detail', pk=pet_pk)
    else:
        form = AdoptionRequestForm()
    
    return render(request, 'core/exchange_request_form.html', {
        'form': form,
        'pet': pet
    })

@login_required
def adoption_request_list(request):
    # Get requests where user is either staff or pet owner
    requests = AdoptionRequest.objects.filter(
        Q(pet__owner=request.user) | Q(requester=request.user)
    ).order_by('-request_date')
    
    return render(request, 'core/adoption_request_list.html', {
        'requests': requests,
        'is_pet_owner': True if requests.filter(pet__owner=request.user).exists() else False
    })

@login_required
def adoption_request_response(request, pk):
    adoption_request = get_object_or_404(AdoptionRequest, pk=pk)
    
    # Check if user is either staff or pet owner
    if not (request.user.is_staff or request.user == adoption_request.pet.owner):
        messages.error(request, 'You do not have permission to respond to this request.')
        return redirect('core:home')
    
    if request.method == 'POST':
        form = AdoptionRequestResponseForm(request.POST, instance=adoption_request)
        if form.is_valid():
            adoption_request = form.save(commit=False)
            adoption_request.response_date = timezone.now()
            adoption_request.save()
            
            # Update pet status if approved
            if adoption_request.status == 'approved':
                adoption_request.pet.adoption_status = 'adopted'
                adoption_request.pet.save()
            
            messages.success(request, 'Adoption request updated successfully!')
            return redirect('core:adoption_request_list')
    else:
        form = AdoptionRequestResponseForm(instance=adoption_request)
    
    return render(request, 'core/adoption_request_response.html', {
        'form': form,
        'adoption_request': adoption_request
    })

# Cart Views
@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'core/cart.html', {'cart': cart})

@login_required
def add_to_cart(request, item_pk):
    # Try to get a marketplace item first
    try:
        item = MarketplaceItem.objects.get(pk=item_pk)
        item_type = 'marketplace'
    except MarketplaceItem.DoesNotExist:
        # If not a marketplace item, try to get a listing
        try:
            item = Listing.objects.get(pk=item_pk)
            if item.listing_type != 'sale':
                messages.error(request, 'Only items for sale can be purchased.')
                return redirect('core:pet_detail', pk=item.pet.id)
            item_type = 'listing'
        except Listing.DoesNotExist:
            messages.error(request, 'Item not found.')
            return redirect('core:marketplace_list')
    
    # For pets listed for sale, redirect directly to checkout
    if item_type == 'listing':
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Remove any existing cart items for this pet
        CartItem.objects.filter(cart=cart, listing=item).delete()
        
        # Create a new cart item
        CartItem.objects.create(
            cart=cart,
            listing=item,
            quantity=1
        )
        
        messages.success(request, 'Pet added to cart! Proceeding to checkout...')
        return redirect('core:checkout')
    
    # For marketplace items, proceed with normal cart addition
    cart, created = Cart.objects.get_or_create(user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > item.stock:
        messages.error(request, 'Requested quantity exceeds available stock.')
        return redirect('marketplace:detail', pk=item_pk)
    
    # Remove any existing cart items for this marketplace item
    CartItem.objects.filter(cart=cart, marketplace_item=item).delete()
    
    # Create a new cart item
    CartItem.objects.create(
        cart=cart,
        marketplace_item=item,
        quantity=quantity
    )
    
    messages.success(request, f'{quantity} x {item.name} added to cart!')
    return redirect('marketplace:cart')

@login_required
def remove_from_cart(request, item_pk):
    cart = get_object_or_404(Cart, user=request.user)
    try:
        # Try to find cart item with marketplace_item
        cart_item = CartItem.objects.get(cart=cart, marketplace_item_id=item_pk)
    except CartItem.DoesNotExist:
        try:
            # Try to find cart item with listing
            cart_item = CartItem.objects.get(cart=cart, listing_id=item_pk)
        except CartItem.DoesNotExist:
            messages.error(request, 'Item not found in cart.')
            return redirect('core:cart_view')
    
    cart_item.delete()
    messages.success(request, 'Item removed from cart!')
    return redirect('core:cart_view')

# Order Views
@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    if not cart.items.exists():
        messages.error(request, 'Your cart is empty!')
        return redirect('core:marketplace_list')
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = cart.total_price
            order.save()
            
            # Create order items and handle pet transfers
            for cart_item in cart.items.all():
                if cart_item.marketplace_item:
                    # Handle marketplace items
                    OrderItem.objects.create(
                        order=order,
                        item=cart_item.marketplace_item,  # Changed from marketplace_item to item
                        quantity=cart_item.quantity,
                        price_at_time=cart_item.marketplace_item.price
                    )
                    # Update stock
                    cart_item.marketplace_item.stock -= cart_item.quantity
                    cart_item.marketplace_item.save()
                elif cart_item.listing:
                    # For pet listings, we need to create a marketplace item first
                    pet = cart_item.listing.pet
                    marketplace_item = MarketplaceItem.objects.create(
                        name=f"Pet: {pet.name}",
                        description=f"Pet purchase: {pet.name} ({pet.get_type_display()})",
                        price=pet.price,
                        stock=1,
                        category='other',
                        shop_owner=pet.owner
                    )
                    # Create order item with the marketplace item
                    OrderItem.objects.create(
                        order=order,
                        item=marketplace_item,  # Use the created marketplace item
                        quantity=1,
                        price_at_time=pet.price
                    )
                    # Transfer pet ownership
                    pet.owner = request.user
                    pet.save()
                    # Update listing status
                    cart_item.listing.status = 'sold'
                    cart_item.listing.save()
            
            # Clear cart
            cart.items.all().delete()
            
            messages.success(request, 'Order placed successfully!')
            return redirect('core:order_detail', pk=order.pk)
    else:
        form = OrderForm()
    
    return render(request, 'core/checkout.html', {
        'form': form,
        'cart': cart
    })

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'core/order_list.html', {'orders': orders})

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'core/order_detail.html', {'order': order})

@login_required
def order_cancel(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    if order.status == 'pending':
        order.status = 'cancelled'
        order.save()
        
        # Restore stock for each item
        for order_item in order.orderitem_set.all():  # Changed from order.items.all() to order.orderitem_set.all()
            marketplace_item = order_item.item  # This is now correct as item is the field name in OrderItem model
            marketplace_item.stock += order_item.quantity
            marketplace_item.save()
        
        messages.success(request, 'Order cancelled successfully.')
    else:
        messages.error(request, 'Only pending orders can be cancelled.')
    
    return redirect('core:order_detail', pk=order.pk)

# Shop Owner Dashboard
@login_required
def shop_owner_dashboard(request):
    if not request.user.marketplace_items.exists():
        messages.error(request, 'You do not have any items listed.')
        return redirect('core:marketplace_list')
    
    items = request.user.marketplace_items.all()
    orders = Order.objects.filter(items__shop_owner=request.user).distinct()
    
    return render(request, 'core/shop_owner_dashboard.html', {
        'items': items,
        'orders': orders
    })

# Lost & Found Views
@login_required
def lost_found_list(request):
    search_query = request.GET.get('search', '')
    status = request.GET.get('status', '')
    date = request.GET.get('date', '')
    
    lost_pets = LostFound.objects.filter(status='lost')
    found_pets = LostFound.objects.filter(status='found')
    
    if search_query:
        lost_pets = lost_pets.filter(
            Q(title__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(description__icontains=search_query)
        )
        found_pets = found_pets.filter(
            Q(title__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    if date:
        lost_pets = lost_pets.filter(date=date)
        found_pets = found_pets.filter(date=date)
    
    if status:
        if status == 'lost':
            found_pets = LostFound.objects.none()
        elif status == 'found':
            lost_pets = LostFound.objects.none()
    
    return render(request, 'core/lost_found_list.html', {
        'lost_pets': lost_pets,
        'found_pets': found_pets
    })

@login_required
def lost_pet(request):
    if request.method == 'POST':
        form = LostPetForm(request.POST, request.FILES)
        if form.is_valid():
            lost_pet = form.save(commit=False)
            lost_pet.user = request.user
            lost_pet.status = 'lost'
            
            # Create a new Pet entry
            pet = Pet.objects.create(
                name=form.cleaned_data['pet_name'],
                type=form.cleaned_data['pet_type'],
                breed=form.cleaned_data['breed'],
                age=form.cleaned_data['age'],
                gender=form.cleaned_data['gender'],
                owner=request.user,
                description=f"Lost pet reported on {timezone.now().strftime('%Y-%m-%d')}"
            )
            
            # Link the pet to the lost report
            lost_pet.pet = pet
            lost_pet.save()
            
            messages.success(request, 'Lost pet report has been submitted successfully.')
            return redirect('core:lost_found_list')
    else:
        form = LostPetForm()
    
    return render(request, 'core/lost_pet_form.html', {'form': form})

@login_required
def found_pet(request):
    if request.method == 'POST':
        form = FoundPetForm(request.POST, request.FILES)
        if form.is_valid():
            found_pet = form.save(commit=False)
            found_pet.user = request.user
            found_pet.status = 'found'
            
            # Create a new Pet entry
            pet = Pet.objects.create(
                name=f"Found {form.cleaned_data['pet_type'].title()}",
                type=form.cleaned_data['pet_type'],
                breed=form.cleaned_data['breed'],
                age=form.cleaned_data['age'],
                gender=form.cleaned_data['gender'],
                owner=request.user,
                description=f"Found pet reported on {timezone.now().strftime('%Y-%m-%d')}"
            )
            
            # Link the pet to the found report
            found_pet.pet = pet
            found_pet.save()
            
            messages.success(request, 'Found pet report has been submitted successfully.')
            return redirect('core:lost_found_list')
    else:
        form = FoundPetForm()
    
    return render(request, 'core/found_pet_form.html', {'form': form})

@login_required
def lost_pet_detail(request, pk):
    lost_pet = get_object_or_404(LostFound, pk=pk, status='lost')
    return render(request, 'lost_found/lostfound_detail.html', {'item': lost_pet})

@login_required
def found_pet_detail(request, pk):
    found_pet = get_object_or_404(LostFound, pk=pk, status='found')
    return render(request, 'lost_found/lostfound_detail.html', {'item': found_pet})

@login_required
def lost_pet_update(request, pk):
    lost_pet = get_object_or_404(LostFound, pk=pk, status='lost', user=request.user)
    if request.method == 'POST':
        form = LostPetForm(request.POST, request.FILES, instance=lost_pet)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lost pet report updated successfully!')
            return redirect('lost_found:detail', pk=lost_pet.pk)
    else:
        form = LostPetForm(instance=lost_pet)
    return render(request, 'lost_found/lostfound_form.html', {'form': form})

@login_required
def found_pet_update(request, pk):
    found_pet = get_object_or_404(LostFound, pk=pk, status='found', user=request.user)
    if request.method == 'POST':
        form = FoundPetForm(request.POST, request.FILES, instance=found_pet)
        if form.is_valid():
            form.save()
            messages.success(request, 'Found pet report updated successfully!')
            return redirect('lost_found:detail', pk=found_pet.pk)
    else:
        form = FoundPetForm(instance=found_pet)
    return render(request, 'lost_found/lostfound_form.html', {'form': form})

@login_required
def lost_pet_delete(request, pk):
    lost_pet = get_object_or_404(LostFound, pk=pk, status='lost', user=request.user)
    if request.method == 'POST':
        lost_pet.delete()
        messages.success(request, 'Lost pet report deleted successfully!')
        return redirect('lost_found:list')
    return render(request, 'lost_found/lostfound_confirm_delete.html', {'item': lost_pet})

@login_required
def found_pet_delete(request, pk):
    found_pet = get_object_or_404(LostFound, pk=pk, status='found', user=request.user)
    if request.method == 'POST':
        found_pet.delete()
        messages.success(request, 'Found pet report deleted successfully!')
        return redirect('lost_found:list')
    return render(request, 'lost_found/lostfound_confirm_delete.html', {'item': found_pet})
