from django.shortcuts import render
from django.contrib.auth.models import User
from store.models import *
from django.contrib.auth.decorators import user_passes_test

def admin_required(view):
    return user_passes_test(lambda u: u.is_staff)(view)


    

@admin_required
def dashboard_home(request):
    return render(request, 'dashboard/home.html', {
        'users': User.objects.count(),
        'orders': Order.objects.count(),
        'sales': sum(o.total for o in Order.objects.all())
    })
    
  
@admin_required
def users_list(request):
    return render(request, 'dashboard/users.html', {'users': User.objects.all()})


@admin_required
def orders_list(request):
    return render(request, 'dashboard/orders.html', {'orders': Order.objects.all()})


@admin_required
def products_list(request):
    return render(request, 'dashboard/products.html', {'products': Product.objects.all()}) 


from django.shortcuts import render

def login_view(request):
    return render(request, 'auth/login.html')

def signup_view(request):
    return render(request, 'auth/signup.html')

def dashboard(request):
    return render(request, 'dashboard/dashboard.html')