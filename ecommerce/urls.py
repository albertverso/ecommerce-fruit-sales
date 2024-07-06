from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_fruits),
    path('login/', views.login_user)
]