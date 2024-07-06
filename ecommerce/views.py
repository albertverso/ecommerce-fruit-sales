from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.
def register_fruits(request):
    if request.method == "GET":
        return render(request, 'register_fruits.html')
    elif request.method == "POST":
        name = request.POST.get('name_fruit')
        price = request.POST.get('price_fruit')
        return HttpResponse(f'{name} - {price}')

def login_user(request):
    if request.method == "GET":
        return render(request, 'login_user.html')
    elif request.method == "POST":
        username = request.POST.get('user_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.get(username=username)

        if user: 
            return HttpResponse('Ja existe um usuario com esse nome')
        
        return HttpResponse(f'{username} - {email} - {password}')