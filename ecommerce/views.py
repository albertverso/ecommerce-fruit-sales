from django.shortcuts import render, redirect
from ecommerce.models import User, Fruit, Sale, SaleItem
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from ecommerce.forms import UserProfileForm
from django.contrib import messages
from django.contrib.messages import get_messages
import time
# Create your views here.

def sigh_up(request):
    if request.method == "GET":
        return render(request, 'sigh_up.html')
    elif request.method == "POST":
        username = request.POST.get('user_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(username=username).first()

        if user: 
            return HttpResponse('Ja existe um usuario com esse nome')
      
        user_created = User.objects.create(username=username, email=email)
        user_created.set_password(password)  # Criptografa a senha
        user_created.save()

        return HttpResponse(f'{user_created}')

def sigh_in(request):
    
    if request.method == "GET":
        return render(request, 'sigh_in.html')
    elif request.method == "POST":
        print(request.POST.get('user_name'))
        username = request.POST.get('user_name')
        password = request.POST.get('password')

        user = User.objects.get(username=username)

        user = authenticate(username=username, password=password)
        if user: 
         
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse('username ou senha invalida')

@login_required(login_url="/ecommerce/sigh_in")
def home_page(request):
               
    if request.method == "GET":
        form = UserProfileForm(instance=request.user)

        user = request.user

        fruits_list = Fruit.objects.all()
        user_list = User.objects.filter(role__in=['cliente', 'vendedor'])

        print(user.username)
        if user.role == 'Cliente':
            context = {
                'is_cliente': True,
                'fruits': fruits_list
                }
            return render(request, 'home.html', context)
        elif user.role == 'Vendedor':
            context = {
                'is_cliente': True,
                'fruits': fruits_list
                }
            return render(request, 'home.html', context)
        elif user.role == 'Admin':
            context = {
            'is_admin': True,
            'fruits': fruits_list,
            'list_user': user_list,
            'user': user,
            'form': form,
            'messages': get_messages(request)
            }
            return render(request, 'home.html', context ) 
        else:
            return HttpResponse("Access Denied")
    elif request.method == "POST":
            if 'logout' in request.POST:
                logout(request)
                return redirect('home')   

            if 'edit_user' in request.POST:
                form = UserProfileForm(request.POST, instance=request.user)
                if form.is_valid():
                    form.save()

                    messages.success(request, 'Profile updated successfully')
                    return redirect('home')
        
          

def register_fruits(request):
    if request.method == "GET":
        return render(request, 'register_fruits.html')
    elif request.method == "POST":
        name = request.POST.get('name_fruit')
        price = request.POST.get('price_fruit')
        return HttpResponse(f'{name} - {price}')