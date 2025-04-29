from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MarketplaceItem, PetListing
from .forms import MarketplaceItemForm, PetListingForm

@login_required
def marketplace_item_list(request):
    items = MarketplaceItem.objects.all()
    return render(request, 'marketplace/item_list.html', {'items': items})

@login_required
def marketplace_item_create(request):
    if request.method == 'POST':
        form = MarketplaceItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.seller = request.user
            item.save()
            messages.success(request, 'Item created successfully!')
            return redirect('marketplace:list')
    else:
        form = MarketplaceItemForm()
    return render(request, 'marketplace/item_form.html', {
        'form': form,
        'title': 'Add New Item'
    })

@login_required
def marketplace_item_detail(request, pk):
    item = get_object_or_404(MarketplaceItem, pk=pk)
    return render(request, 'marketplace/item_detail.html', {'item': item})

@login_required
def marketplace_item_update(request, pk):
    item = get_object_or_404(MarketplaceItem, pk=pk)
    if request.user != item.seller:
        messages.error(request, 'You do not have permission to edit this item.')
        return redirect('marketplace:detail', pk=pk)
    
    if request.method == 'POST':
        form = MarketplaceItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item updated successfully!')
            return redirect('marketplace:detail', pk=pk)
    else:
        form = MarketplaceItemForm(instance=item)
    return render(request, 'marketplace/item_form.html', {
        'form': form,
        'title': 'Edit Item'
    })

@login_required
def marketplace_item_delete(request, pk):
    item = get_object_or_404(MarketplaceItem, pk=pk)
    if request.user != item.seller:
        messages.error(request, 'You do not have permission to delete this item.')
        return redirect('marketplace:detail', pk=pk)
    
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item deleted successfully!')
        return redirect('marketplace:list')
    return render(request, 'marketplace/item_confirm_delete.html', {'item': item})

@login_required
def cart(request):
    return render(request, 'marketplace/cart.html')

@login_required
def add_to_cart(request, item_id):
    # Add item to cart logic here
    return redirect('marketplace:cart')

@login_required
def remove_from_cart(request, item_id):
    # Remove item from cart logic here
    return redirect('marketplace:cart')

@login_required
def pet_listing_list(request):
    listings = PetListing.objects.filter(status='available')
    return render(request, 'marketplace/pet_listing_list.html', {'listings': listings})

@login_required
def pet_listing_create(request):
    if request.method == 'POST':
        form = PetListingForm(request.POST, user=request.user)
        if form.is_valid():
            listing = form.save()
            messages.success(request, 'Pet listed successfully!')
            return redirect('marketplace:pet_listing_detail', pk=listing.pk)
    else:
        form = PetListingForm(user=request.user)
    return render(request, 'marketplace/pet_listing_form.html', {
        'form': form,
        'title': 'List Pet for Sale'
    })

@login_required
def pet_listing_detail(request, pk):
    listing = get_object_or_404(PetListing, pk=pk)
    return render(request, 'marketplace/pet_listing_detail.html', {'listing': listing})

@login_required
def pet_listing_purchase(request, pk):
    listing = get_object_or_404(PetListing, pk=pk)
    
    if listing.status != 'available':
        messages.error(request, 'This pet is no longer available for purchase.')
        return redirect('marketplace:pet_listing_detail', pk=pk)
    
    if listing.seller == request.user:
        messages.error(request, 'You cannot purchase your own pet.')
        return redirect('marketplace:pet_listing_detail', pk=pk)
    
    if request.method == 'POST':
        listing.status = 'pending'
        listing.buyer = request.user
        listing.save()
        messages.success(request, 'Purchase request sent successfully!')
        return redirect('marketplace:pet_listing_detail', pk=pk)
    
    return render(request, 'marketplace/pet_listing_confirm_purchase.html', {'listing': listing})
