from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register_fruits/', views.register_fruits, name='register'),
    path('sigh_up/', views.sigh_up, name='sign_up'),
    path('login_user/', views.sigh_in, name='login_user'),
    path('home/', views.home_page, name='home') ,
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)