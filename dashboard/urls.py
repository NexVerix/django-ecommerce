from django.urls import path
from . import views

urlpatterns = [
    # path('', views.dashboard_home),
    path('users/', views.users_list, name='users'),
    path('orders/', views.orders_list, name='orders'),
    path('products/', views.products_list, name='products'),
     path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.dashboard_home, name='dashboard'),

]