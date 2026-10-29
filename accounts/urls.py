from django.urls import path
from . import views


urlpatterns = [
    path('',views.home,name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path(
        'provider/dashboard/',
        views.provider_dashboard,
        name='provider_dashboard'
    ),

    path(
        'customer/dashboard/',
        views.customer_dashboard,
        name='customer_dashboard'
    ),
]