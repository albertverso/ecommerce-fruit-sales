from django.shortcuts import render, redirect
from ecommerce.models import User, Fruit, Sale, SaleItem
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from ecommerce.forms import UserProfileForm, FruitForm, SaleForm, SaleItemFormSet, FrutaFilterForm
from django.contrib import messages
from django.contrib.messages import get_messages
import time
from django.forms import modelformset_factory
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

def login_user(request):
    
    if request.method == "GET":
        context = {
                'messages': get_messages(request)
                }
        return render(request, 'login_user.html', context)
    elif request.method == "POST":

        if 'sigh_in' in request.POST
            username = request.POST.get('user_name')
            password = request.POST.get('password')

            user = User.objects.get(username=username)

            user = authenticate(username=username, password=password)
            if user: 
            
                login(request, user)
                return redirect('home')
            else:
                return messages.error(request, 'username ou senha invalida')

        elif 'sigh_up' in request.POST
            username = request.POST.get('user_name')
            email = request.POST.get('email')
            password = request.POST.get('password')

            user = User.objects.filter(username=username).first()

            if user: 
                return messages.error(request, 'Ja existe um usuario com esse nome')
        
            user_created = User.objects.create(username=username, email=email)
            user_created.set_password(password)  # Criptografa a senha
            user_created.save()

            messages.success(request, 'Profile created successfully')

            time.sleep(2.5)
            return redirect('home')

@login_required(login_url="/ecommerce/login_user")
def home_page(request):

    if request.method == "GET":
        form_user = UserProfileForm(instance=request.user)
        fruit_form = FruitForm()
        sale_form = SaleForm()
        sale_item_formset = SaleItemFormSet()

        user = request.user
       
        user_list = User.objects.filter(role__in=['cliente', 'vendedor'])

        sales_list = Sale.objects.filter(user=request.user)

        items_list = SaleItem.objects.filter(sale__user=request.user)

        query = request.GET.get('search')

        fruits_list = Fruit.objects.all()

        if query:
            fruits_list = Fruit.objects.filter(fruit_name__icontains=query)
        else:
            fruits_list = Fruit.objects.all()
            if 'search' in request.GET:
                return redirect('home')
        
        if user.role == 'Cliente':
            context = {
                'is_cliente': True,
                'form': form_user,
                'fruits': fruits_list,
                'filter': filter_form_fruit,
                'messages': get_messages(request)
                }
            return render(request, 'home.html', context)

        elif user.role == 'Vendedor': 
            context = {
                'is_vendedor': True,
                'fruits': fruits_list,
                'form': form_user,
                'sale_form': sale_form, 
                'sale_item_formset': sale_item_formset,
                'list_sales': sales_list,
                'items_list': items_list,
                'messages': get_messages(request)
                }
            return render(request, 'home.html', context)

        elif user.role == 'Admin':
            context = {
            'is_admin': True,
            'fruits': fruits_list,
            'filter': filter_form_fruit,
            'list_user': user_list,
            'user': user,
            'form': form_user,
            'fruit_form': fruit_form,
            'messages': get_messages(request)
            }
            return render(request, 'home.html', context ) 
        else:
            return HttpResponse("Access Denied")
    elif request.method == "POST":

            if 'logout' in request.POST:
                logout(request)
                return redirect('home')   

            elif 'edit_user' in request.POST:
                form = UserProfileForm(request.POST, instance=request.user)
                if form.is_valid():
                    form.save()

                    messages.success(request, 'Profile updated successfully')
                    return redirect('home')

            elif 'added-user' in request.POST:
                username = request.POST.get('username')
                email = request.POST.get('email')
                password = request.POST.get('password')
                role = request.POST.get('role')

                user = User.objects.filter(username=username).first()

                if user: 
                    return messages.error(request, 'Username já existe')
            
                user_created = User.objects.create(username=username, email=email, role=role)
                user_created.set_password(password)  # Criptografa a senha
                user_created.save()

                messages.success(request, 'Profile created successfully')

                return redirect('home')
            elif 'added-fruit' in request.POST:

                fruit_form = FruitForm(request.POST, request.FILES)

                if fruit_form.is_valid():
                    fruit_form.save()
                    messages.success(request, 'Fruit created successfully')
                    return redirect('home')


            elif 'items-sale' in request.POST:
                sale_form = SaleForm(request.POST)
                sale_item_formset = SaleItemFormSet(request.POST)
                
                if sale_form.is_valid() and sale_item_formset.is_valid():
                    sale = sale_form.save(commit=False)
                    sale.user = request.user
                    sale.save()
                    
                    sale_items = sale_item_formset.save(commit=False)
                    for item in sale_items:
                        item.sale = sale
                        item.save()

                    messages.success(request, 'Sale successfully')
                    return redirect('home')