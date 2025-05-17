from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models import MarketplaceItem
from .forms import MarketplaceItemForm

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
            item.shop_owner = request.user
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
    if request.user != item.shop_owner:
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
    if request.user != item.shop_owner:
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
