from django.contrib import admin
from .models import User, Fruit, Sale, SaleItem
# Register your models here.

admin.site.register(User)
admin.site.register(Fruit)
admin.site.register(Sale)
admin.site.register(SaleItem)