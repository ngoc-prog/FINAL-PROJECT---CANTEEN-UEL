from django.urls import path
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"), 
    path('home/', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('login/', views.loginPage, name="login"),
    path('search/', views.search , name="search"),
    path('detail/', views.detail, name='detail'),
    path('category/', views.category, name="category"),
    path('logout/', views.logoutPage, name="logout"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('updateitem/', views.updateItem, name='updateitem'),
    path('profile/', views.profile, name='profile'),
    path('favorites/', views.favorites, name='favorites'),
    path('history/', views.history, name='history'),
    path('contact/', views.contact, name='contact'),
    path('qr/', views.qr, name='qr'),
    path('clear_cart/', views.clear_cart, name="clear_cart"),
]

