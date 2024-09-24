# E-commerce de Frutas - Django Project
- Este projeto é um sistema de E-commerce de Frutas desenvolvido em Django. O objetivo principal é permitir que administradores gerenciem o cadastro de frutas disponíveis para venda, criem usuários com perfis de vendedores, e acompanhem todas as vendas realizadas na plataforma. Já os vendedores têm acesso às frutas disponíveis para vendê-las. O sistema registra todas as vendas realizadas por cada vendedor.

# Funcionalidades
## Para o Administrador:
- Cadastro, edição e exclusão de frutas disponíveis para venda.
- Criação e gerenciamento de usuários, com perfis de vendedor e cliente (consumidor).
- Acesso a todos os usuários cadastrados no sistema.
## Para Vendedores:
- Visualização das frutas cadastradas no sistema pelo administrador.
- Realização de vendas de frutas disponíveis.
- Registro de cada venda realizada, associada ao vendedor.
## Para Clientes:
- Acesso ao catálogo de frutas (função de consumidor).
- Realização de compras.
- 
# Tecnologias Utilizadas
- Django: Framework web usado para o desenvolvimento do backend.
- PostgreSQL: Bancos de dados usados para armazenar informações sobre frutas, usuários e vendas.
- Cloudinary: Serviço de hospedagem de imagens para armazenar fotos das frutas.
- Gunicorn: Servidor WSGI para deployment.
- Whitenoise: Para servir arquivos estáticos.
- Pillow: Biblioteca para manipulação de imagens no Django.
 
# Requisitos do Sistema
- Para rodar o projeto localmente, você precisará dos seguintes pacotes Python instalados:

````
asgiref==3.8.1
dj-database-url==2.2.0
Django==5.0.6
gunicorn==23.0.0
mysqlclient==2.2.4
packaging==24.1
pillow==10.4.0
psycopg2-binary==2.9.9
python-dotenv==1.0.1
sqlparse==0.5.0
typing_extensions==4.12.2
tzdata==2024.1
whitenoise==6.7.0
cloudinary==1.41.0
django-cloudinary-storage==0.3.0
````

# Configuração do Projeto
- Clone o repositório para o seu ambiente local:
````
git clone https://github.com/albertverso/ecommerce-fruit-sales.git
cd ecommerce-de-frutas
````

Instale as dependências:
````
pip install -r requirements.txt
````

## Configure suas variáveis de ambiente no arquivo .env. Certifique-se de incluir as credenciais de banco de dados e de integração com o Cloudinary.

# Realize as migrações do banco de dados:
````
python manage.py migrate
````

# Crie um superusuário para acessar o painel de administração do Django:
````
python manage.py createsuperuser
````
# Inicie o ambiente virtual:
````
./venv/Scripts/activate  
````

# Inicie o servidor de desenvolvimento:
````
python manage.py runserver
````

# Como Usar
- Acesse o painel de administração em http://localhost:8000/admin/ com as credenciais do superusuário criado.
- No painel de administração, cadastre novas frutas e crie usuários com perfis de vendedor ou cliente.
- Os vendedores podem acessar o sistema para visualizar as frutas e registrar vendas.

# Deploy
 https://ecommerce-fruit-sales.onrender.com/

# Licença
Este projeto é de código aberto e está licenciado sob os termos da MIT License.
