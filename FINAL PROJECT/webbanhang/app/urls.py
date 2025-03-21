from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views


# Group all URL patterns in a single file
urlpatterns = [
    # Admin URL

    

    # Main/Home URLs
    path('', views.home, name="home"), 
    path('home/', views.home, name="home"),
    path('fullmenu/', views.fullmenu, name="fullmenu"),
    path('contact/', views.contact, name='contact'),

    # Auth URLs
    path('register/', views.register, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name="logout"),
    path('profile/', views.profile, name='profile'),

    # Product & Category URLs  
    path('search/', views.search, name="search"),
    path('detail/', views.detail, name='detail'),
    path('category/', views.category, name="category"),
    path('submit_feedback/', views.submit_feedback, name='submit_feedback'),

    # Cart URLs
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name='update_item'),
    path('clear_cart/', views.clear_cart, name="clear_cart"),
] 

