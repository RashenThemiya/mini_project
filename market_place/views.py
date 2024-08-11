from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, ProfileForm, ItemForm
from .models import CustomUser, Profile, Item, Cart, CartItem, Order
from .forms import AddToCartForm
def index(request):
    # Fetch all items by default
    items = Item.objects.all()
    
    # Handle search query
    search_query = request.GET.get('search', '')
    if search_query:
        items = items.filter(name__icontains=search_query)
    
    # Handle filter options
    category_filter = request.GET.get('category', '')
    if category_filter:
        items = items.filter(category=category_filter)
    
    user_type = None
    if request.user.is_authenticated:
        user_type = request.user.profile.user_type

    context = {
        'items': items,
        'user_type': user_type,
        'search_query': search_query,
        'category_filter': category_filter,
    }
    return render(request, 'market_place.html', context)

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('market_place_index')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileForm()
    
    return render(request, 'register.html', {'user_form': user_form, 'profile_form': profile_form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('market_place_index')
        else:
            messages.error(request, "Invalid login credentials.")
    return render(request, 'login.html')

@login_required
def add_to_cart(request, item_id):
    item = Item.objects.get(id=item_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    form = AddToCartForm(request.POST or None)

    if form.is_valid():
        quantity = form.cleaned_data['quantity']
        cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
        
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

        messages.success(request, f"{item.name} added to cart with quantity {quantity}.")
    
    return redirect('market_place_index')

@login_required
def add_to_cart(request, item_id):
    item = Item.objects.get(id=item_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    quantity = int(request.POST.get('quantity', 1))  # Get quantity from POST data
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    else:
        cart_item.quantity = quantity
        cart_item.save()
    
    messages.success(request, f"{item.name} added to cart with quantity {quantity}.")
    return redirect('cart')

@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    
    return render(request, 'cart.html', {'cart_items': cart_items})

@login_required
def place_order(request):
    cart = Cart.objects.get(user=request.user)
    order = Order.objects.create(buyer=request.user.profile)
    
    for item in cart.cartitem_set.all():  # Use related_name for cart items
        order.items.add(item.item)
    
    cart.cartitem_set.all().delete()  # Clear cart items
    
    messages.success(request, "Order placed successfully.")
    return redirect('market_place_index')
def add_item(request):
    if request.user.profile.user_type != 'seller':
        return redirect('market_place_index')
    
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.seller = request.user.profile
            item.save()
            messages.success(request, "Item added successfully.")
            return redirect('market_place_index')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ItemForm()
    
    return render(request, 'add_item.html', {'form': form})