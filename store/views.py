import requests
import stripe
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import *

stripe.api_key = "YOUR_SECRET_KEY"

# ---------------- PRODUCTS ----------------
def fetch_products():
    return requests.get("https://fakestoreapi.com/products").json()


def home(request):
    """Home page with product listing and filters."""
    products = fetch_products()

    q = request.GET.get('q')
    category = request.GET.get('category')
    min_price = request.GET.get('min')
    max_price = request.GET.get('max')

    if q:
        products = [p for p in products if q.lower() in p['title'].lower()]
    if category:
        products = [p for p in products if p['category'] == category]
    if min_price:
        products = [p for p in products if p['price'] >= float(min_price)]
    if max_price:
        products = [p for p in products if p['price'] <= float(max_price)]

    categories = list(set([p['category'] for p in fetch_products()]))

    return render(request, 'store/home.html', {'products': products, 'categories': categories})

# ---------------- AUTH ----------------
def signup_view(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('/')
    return render(request, 'store/signup.html', {'form': form})


def login_view(request):
    form = AuthenticationForm(data=request.POST or None)
    if form.is_valid():
        login(request, form.get_user())
        return redirect('/')
    return render(request, 'store/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')

# ---------------- CART ----------------
@login_required(login_url='/login/')
def add_to_cart(request, product_id):
    """Add product to cart or increase quantity."""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    data = requests.get(f"https://fakestoreapi.com/products/{product_id}").json()

    product, _ = Product.objects.get_or_create(
        title=data['title'],
        defaults={'price': data['price'], 'image': data['image'], 'category': data['category']}
    )

    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()

    return redirect('cart')


@login_required(login_url='/login/')
def cart_view(request):
    """Show the current user's cart items."""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    total = sum(i.product.price * i.quantity for i in items)
    return render(request, 'store/cart.html', {'items': items, 'total': total})


@login_required(login_url='/login/')
def update_quantity(request, item_id):
    """Update quantity of a cart item."""
    item = CartItem.objects.get(id=item_id)
    qty = int(request.POST.get('quantity'))
    if qty > 0:
        item.quantity = qty
        item.save()
    return redirect('cart')


@login_required(login_url='/login/')
def remove_from_cart(request, item_id):
    """Remove item from cart."""
    CartItem.objects.get(id=item_id).delete()
    return redirect('cart')


# ---------------- STRIPE ----------------
@login_required(login_url='/login/')
def create_checkout_session(request):
    """Create a Stripe checkout session."""
    cart = Cart.objects.get(user=request.user)
    items = CartItem.objects.filter(cart=cart)

    line_items = []
    for i in items:
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': i.product.title},
                'unit_amount': int(i.product.price * 100),
            },
            'quantity': i.quantity,
        })

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url='http://127.0.0.1:8000/success/',
        cancel_url='http://127.0.0.1:8000/cart/',
    )

    return JsonResponse({'id': session.id})


# ---------------- ORDER ----------------
@login_required(login_url='/login/')
def success(request):
    """Order success page and create Order/OrderItems."""
    cart = Cart.objects.get(user=request.user)
    items = CartItem.objects.filter(cart=cart)

    total = sum(i.product.price * i.quantity for i in items)
    order = Order.objects.create(user=request.user, total=total)

    for i in items:
        OrderItem.objects.create(
            order=order,
            product=i.product.title,
            price=i.product.price,
            quantity=i.quantity
        )

    items.delete()
    return render(request, 'store/success.html')


@login_required(login_url='/login/')
def order_history(request):
    """View order history for the logged-in user."""
    orders = Order.objects.filter(user=request.user)
    return render(request, 'store/orders.html', {'orders': orders})