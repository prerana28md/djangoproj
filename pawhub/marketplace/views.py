from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models import MarketplaceItem, Listing, Cart, CartItem, Order
from core.forms import ListingForm, CartItemForm
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
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'marketplace/cart.html', {'cart': cart})

@login_required
def add_to_cart(request, item_id):
    try:
        item = MarketplaceItem.objects.get(pk=item_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, marketplace_item=item)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        messages.success(request, 'Item added to cart!')
    except MarketplaceItem.DoesNotExist:
        messages.error(request, 'Item not found.')
    return redirect('marketplace:cart')

@login_required
def remove_from_cart(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, marketplace_item_id=item_id)
    cart_item.delete()
    messages.success(request, 'Item removed from cart!')
    return redirect('marketplace:cart')

@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated successfully!')
        else:
            cart_item.delete()
            messages.success(request, 'Item removed from cart!')
    
    return redirect('marketplace:cart')

@login_required
def pet_listing_list(request):
    listings = Listing.objects.filter(listing_type='sale', status='available')
    return render(request, 'marketplace/pet_listing_list.html', {'listings': listings})

@login_required
def pet_listing_create(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.listing_type = 'sale'
            listing.status = 'available'
            listing.save()
            messages.success(request, 'Pet listed for sale successfully!')
            return redirect('marketplace:pet_listing_list')
    else:
        form = ListingForm(user=request.user)
    return render(request, 'marketplace/pet_listing_form.html', {'form': form})

@login_required
def pet_listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk, listing_type='sale')
    return render(request, 'marketplace/pet_listing_detail.html', {'listing': listing})

@login_required
def shop_dashboard(request):
    user_items = MarketplaceItem.objects.filter(shop_owner=request.user)
    return render(request, 'marketplace/shop_dashboard.html', {
        'items': user_items
    })

@login_required
def shop_orders(request):
    orders = Order.objects.filter(items__marketplace_item__shop_owner=request.user).distinct()
    return render(request, 'marketplace/shop_orders.html', {
        'orders': orders
    })

@login_required
def shop_order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, items__marketplace_item__shop_owner=request.user)
    return render(request, 'marketplace/shop_order_detail.html', {
        'order': order
    })
