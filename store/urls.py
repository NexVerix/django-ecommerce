from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view),

    path('cart/', views.cart_view, name='cart'),
    path('add/<int:product_id>/', views.add_to_cart),

    path('update/<int:item_id>/', views.update_quantity),
    path('remove/<int:item_id>/', views.remove_from_cart),

    path('checkout/', views.create_checkout_session),
    path('success/', views.success),
    path('orders/', views.order_history),
]