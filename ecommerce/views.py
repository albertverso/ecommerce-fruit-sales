from django.shortcuts import render, redirect, get_object_or_404
from ecommerce.models import User, Fruit, Sale, SaleItem
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from ecommerce.forms import UserProfileForm, FruitForm, SaleForm, SaleItemFormSet
from django.contrib import messages
from django.contrib.messages import get_messages
from PIL import Image
import cloudinary
import cloudinary.uploader
import cloudinary.api


def login_user(request):
    """
    Função para gerenciar o login e inscrição de usuários.
    """
    if request.method == "GET":
        # Renderiza a página de login com mensagens
        context = {
            'messages': get_messages(request)
        }
        return render(request, 'login_user.html', context)
    
    elif request.method == "POST":
        if 'sigh_in' in request.POST:
            # Processa o login
            username = request.POST.get('user_name')
            password = request.POST.get('password')

            # Autentica o usuário
            user = authenticate(username=username, password=password)
            if user:
                # Faz login e redireciona para a página inicial
                login(request, user)
                return redirect('home')
            else:
                # Exibe mensagem de erro se a autenticação falhar
                messages.error(request, 'Nome de usuário ou senha inválida')
                return redirect('home')

        elif 'sigh_up' in request.POST:
            # Processa a inscrição de um novo usuário
            username = request.POST.get('user_name')
            email = request.POST.get('email')
            password = request.POST.get('password')

            # Verifica se o nome de usuário já existe
            user = User.objects.filter(username=username).first()
            if user:
                messages.error(request, 'Já existe um usuário com esse nome')
                return redirect('home')

            # Cria um novo usuário
            user_created = User.objects.create(username=username, email=email)
            user_created.set_password(password)  # Criptografa a senha
            user_created.save()

            messages.success(request, 'Conta criada com sucesso')
            return redirect('home')

@login_required(login_url="/ecommerce/login_user")
def home_page(request, id=None):
    """
    Função para gerenciar a página inicial com base no papel do usuário.
    """
    if request.method == "GET":
        # Inicializa formulários e lista de itens
        form_user = UserProfileForm(instance=request.user)
        fruit_form = FruitForm()
        sale_form = SaleForm()
        sale_item_formset = SaleItemFormSet()

        user = request.user
        user_list = User.objects.filter(role__in=['Cliente', 'Vendedor'])
        sales_list = Sale.objects.filter(user=request.user)
        items_list = SaleItem.objects.filter(sale__user=request.user)
        filter_fruit = request.GET.get('filter-class')
        filter_fruit_fresh = request.GET.get('filter-fresh')
        query = request.GET.get('search')
        fruits_list = Fruit.objects.all()

        print(user_list)

        # Filtra a lista de frutas com base nos parâmetros de pesquisa
        if query:
            fruits_list = Fruit.objects.filter(fruit_name__icontains=query)
        elif filter_fruit and filter_fruit_fresh:
            fruits_list = Fruit.objects.filter(rating=filter_fruit, fresh=(filter_fruit_fresh.lower() == 'true'))
        elif filter_fruit:
            fruits_list = Fruit.objects.filter(rating=filter_fruit)
        elif filter_fruit_fresh is not None and filter_fruit_fresh != '':
            fruits_list = Fruit.objects.filter(fresh=(filter_fruit_fresh.lower() == 'true'))
        else:
            fruits_list = Fruit.objects.all()
            if 'search' in request.GET:
                return redirect('home')

        # Obtém parâmetros de consulta para edição
        global get_query_user
        get_query_user = request.GET.get('get-user', '').strip()
        global get_query_fruit
        get_query_fruit = request.GET.get('get-fruit', '').strip()
        
        # Renderiza a página inicial para o cliente
        if user.role == 'Cliente':
            context = {
                'is_cliente': True,
                'form': form_user,
                'fruits': fruits_list,
                'messages': get_messages(request)
            }
            return render(request, 'home.html', context)
        
        # Renderiza a página inicial para o vendedor
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
        
        # Renderiza novamente a página inicial para o administrador (código redundante, mas deixado como está)
        elif user.role == 'Admin':

             # Processa a edição de usuário
            if get_query_user:
                user_instance = get_object_or_404(User, id=get_query_user)
                form = UserProfileForm(instance=user_instance)
                print(user_list)
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
                return render(request, 'home.html', context)
            
            # Processa a edição de fruta
            elif get_query_fruit:
                fruit_instance = get_object_or_404(Fruit, id=get_query_fruit)
                form = FruitForm(instance=fruit_instance)

                context = {
                    'edit_fruit': get_query_fruit,
                    'is_admin': True,
                    'fruits': fruits_list,
                    'list_user': user_list,
                    'user': user,
                    'form': form,
                    'fruit_form': fruit_form,
                    'messages': get_messages(request)
                }
                return render(request, 'home.html', context)
            else:    
                context = {
                    'is_admin': True,
                    'fruits': fruits_list,
                    'list_user': user_list,
                    'user': user,
                    'form': form_user,
                    'fruit_form': fruit_form,
                    'messages': get_messages(request)
                }
                return render(request, 'home.html', context)
        else:
            # Exibe uma mensagem de erro se o papel do usuário não for reconhecido
            return messages.error(request, 'Erro')

    elif request.method == "POST":
        if 'logout' in request.POST:
            # Faz logout e redireciona para a página inicial
            logout(request)
            return redirect('home')

        elif 'edit_user' in request.POST:
            # Processa a edição do perfil do usuário
            form = UserProfileForm(request.POST, instance=request.user)

            if form.is_valid():
                form.save()
                messages.success(request, 'Perfil editado')
                return redirect('home')
            else:
                messages.error(request, 'Erro ao editar o perfil')
                return redirect('home')

        elif 'added-user' in request.POST:
            # Processa a adição de um novo usuário
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            role = request.POST.get('role')

            user = User.objects.filter(username=username).first()
            if user:
                messages.error(request, 'Nome de usuário já existente')
                return redirect('home')

            user_created = User.objects.create(username=username, email=email, role=role)
            user_created.set_password(password)  # Criptografa a senha
            user_created.save()

            messages.success(request, 'Usuário adicionado')
            return redirect('home')

        elif 'added-fruit' in request.POST:
            # Processa a adição de uma nova fruta
            fruit_form = FruitForm(request.POST, request.FILES)

            if fruit_form.is_valid():
                fruit_name = fruit_form.cleaned_data['fruit_name']
                rating = fruit_form.cleaned_data['rating']
                quantity = fruit_form.cleaned_data['quantity']
                itemssalevalue_sale = fruit_form.cleaned_data['itemssalevalue_sale']
                fresh = fruit_form.cleaned_data['fresh']
                imagem = request.FILES.get('image')

                if imagem:
                    # Faz o upload da imagem para o Cloudinary
                    upload_result = cloudinary.uploader.upload(imagem, folder="Fruits")
                    image_url = upload_result.get('url')  # Pega a URL da imagem no Cloudinary

                    fruit = Fruit(fruit_name=fruit_name, rating=rating, fresh=fresh, quantity=quantity, itemssalevalue_sale=itemssalevalue_sale, image=image_url)
                    fruit.save()
                    messages.success(request, 'Fruta adicionada')
                    return redirect('home')
                else:
                    fruit = Fruit(fruit_name=fruit_name, rating=rating, fresh=fresh, quantity=quantity, itemssalevalue_sale=itemssalevalue_sale, image='')
                    fruit.save()
                    messages.success(request, 'Fruta adicionada')
                    return redirect('home')

            messages.error(request, 'Error')
            return redirect('home')

        elif 'items-sale' in request.POST:
            # Processa a adição de uma nova venda
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

                messages.success(request, 'Venda cadastrada')
                return redirect('home')

        elif 'btn-delete-user' in request.POST:
            # Processa a exclusão de um usuário
            user = get_object_or_404(User, id=id)
            user.delete()
            messages.success(request, "Usuário deletado com sucesso.")
            return redirect('home')

        elif 'btn-delete-sale' in request.POST:
            # Processa a exclusão de uma venda
            sale = get_object_or_404(Sale, id=id)
            sale.delete()
            messages.success(request, "Venda deletada com sucesso.")
            return redirect('home')

        elif 'btn-delete-fruit' in request.POST:
            # Processa a exclusão de uma venda
            fruit = get_object_or_404(Fruit, id=id)
            fruit.delete()
            messages.success(request, "Fruta deletada com sucesso.")
            return redirect('home')

        elif 'btn-confirm-edit' in request.POST:
            # Confirma a edição de um usuário
            user_instance = get_object_or_404(User, id=get_query_user)
            form_user = UserProfileForm(request.POST, instance=user_instance)

            if form_user.is_valid():
                form_user.save()
                messages.success(request, "Usuário editado com sucesso.")
                return redirect('home')
            else:
                messages.error(request, "Error")
                return redirect('home')

        elif 'btn-confirm-edit-fruit' in request.POST:
            # Busca a fruta existente pelo ID (supondo que você tenha o ID da fruta no POST)
            fruit_instance = get_object_or_404(Fruit, id=get_query_fruit)
            form_fruit = FruitForm(request.POST, instance=fruit_instance)

            if form_fruit.is_valid():
                # Atualiza os campos da fruta com os dados do formulário
                fruit = form_fruit.save(commit=False)  # Obtém a instância da fruta sem salvar ainda

                # Verifica se o usuário enviou uma nova imagem
                imagem = request.FILES.get('edit_image')

                if imagem:
                    # Faz o upload da nova imagem para o Cloudinary
                    upload_result = cloudinary.uploader.upload(imagem, folder="Fruits")
                    image_url = upload_result.get('url')  # Pega a URL da imagem no Cloudinary
                    fruit.image = image_url  # Atualiza a imagem

                # Salva as alterações da fruta existente
                fruit.save()

                messages.success(request, 'Fruta editada com sucesso')
                return redirect('home')

            # Se o formulário não for válido
            messages.error(request, 'Erro ao editar a fruta.')
            return redirect('home')


        else:
            messages.error(request, 'Error')
            return redirect('home')