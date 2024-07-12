from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login_user/', views.login_user, name='login_user'),
    path('home/', views.home_page, name='home'),
    path('home/<int:id>/', views.home_page, name='delete'),
    path('home/<int:id>/', views.home_page, name='update'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)