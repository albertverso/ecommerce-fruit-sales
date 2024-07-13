from django.shortcuts import render, redirect, get_object_or_404
from ecommerce.models import User, Fruit, Sale, SaleItem
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from ecommerce.forms import UserProfileForm, FruitForm, SaleForm, SaleItemFormSet
from django.contrib import messages
from django.contrib.messages import get_messages
import time
from django.forms import modelformset_factory
# Create your views here.

def login_user(request):
    
    if request.method == "GET":
        context = {
                'messages': get_messages(request)
                }
        return render(request, 'login_user.html', context)
    elif request.method == "POST":

        if 'sigh_in' in request.POST:
            username = request.POST.get('user_name')
            password = request.POST.get('password')

            user = User.objects.get(username=username)

            user = authenticate(username=username, password=password)
            if user: 

                login(request, user)
                return redirect('home')
            else:
                context = {
                'messages': get_messages(request)
                }
                messages.error(request, 'username ou senha invalida')
                return render(request, 'login_user.html', context)

        elif 'sigh_up' in request.POST:

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
            return redirect('home')

class ValorGuardado:
    def __init__(self):
        self.valor = None

    def guardar_valor(self, valor):
        self.valor = valor

    def mostrar_valor(self):
        return self.valor

@login_required(login_url="/ecommerce/login_user")
def home_page(request, id=None):
    valor = ValorGuardado()
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


        global get_query_user
        get_query_user = request.GET.get('get-user', '').strip()

        if get_query_user:
            user_instance = get_object_or_404(User, id=get_query_user)

            form = UserProfileForm(instance=user_instance)

            context = {
            'edit': get_query_user,
            'is_admin': True,
            'fruits': fruits_list,
            'list_user': user_list,
            'user': user,
            'form': form,
            'fruit_form': fruit_form,
            'messages': get_messages(request)
            }
            return render(request, 'home.html', context )
        elif user.role == 'Admin':
            context = {
            'is_admin': True,
            'fruits': fruits_list,
            'list_user': user_list,
            'user': user,
            'form': form_user,
            'fruit_form': fruit_form,
            'messages': get_messages(request)
            }
            return render(request, 'home.html', context )

        
        if user.role == 'Cliente':
            context = {
                'is_cliente': True,
                'form': form_user,
                'fruits': fruits_list,
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
            'edit': get_user_object,
            'is_admin': True,
            'fruits': fruits_list,
            'list_user': user_list,
            'user': user,
            'form': form_user,
            'fruit_form': fruit_form,
            'messages': get_messages(request)
            }
            return render(request, 'home.html', context ) 
        else:
            return messages.error(request, 'Erro')
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
            else:
                messages.error(request, 'Error')
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

        elif 'btn-delete-user' in request.POST:
            user = get_object_or_404(User, id=id)
            user.delete()
            messages.success(request, "Usuário deletado com sucesso.")
            return redirect('home') 


        elif 'btn-delete-sale' in request.POST:
            sale = get_object_or_404(Sale, id=id)
            sale.delete()
            messages.success(request, "Venda deletada com sucesso.")
            return redirect('home') 

        elif 'btn-confirm-edit' in request.POST:
          

            user_instance = get_object_or_404(User, id=get_query_user)

            print(user_instance)

            form_user = UserProfileForm(request.POST ,instance=user_instance)

            if form_user.is_valid():
                form_user.save()
                # redirecionar ou fazer algo após salvar
                messages.success(request, "Usuário editado com sucesso.")
                return redirect('home')
            else:
                return HttpResponse('sdfsdfsdfsdf')

        else:
            messages.error(request, 'Error')
            return redirect('home')