from django.urls import path
from . import views

urlpatterns = [
    path('register_fruits/', views.register_fruits, name='register'),
    path('sigh_up/', views.sigh_up, name='sign_in'),
    path('sigh_in/', views.sigh_in, name='sign_in'),
    path('home/', views.home_page, name='home'),
]