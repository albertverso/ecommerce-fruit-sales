from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
from django.db import models

class User(AbstractUser):
    class UserRole(models.TextChoices):
        ADMIN = 'Admin', 'Admin'
        VENDEDOR = 'Vendedor', 'Vendedor'
        CLIENTE = 'Cliente', 'Cliente'
    role = models.CharField(
        max_length=10,
        choices=UserRole.choices,
        default=UserRole.CLIENTE,
    )

    def __str__(self):
        return self.username

class Fruit(models.Model):
    RATING_CHOICES = [
        ('Extra', 'Extra'),
        ('Primeira', 'Primeira'),
        ('Segunda', 'Segunda'),
        ('Terceira', 'Terceira'),
    ]
    id = models.AutoField(primary_key=True)
    fruit_name = models.CharField(max_length=100)
    rating = models.CharField(max_length=10, choices=RATING_CHOICES)
    fresh = models.BooleanField()
    quantity = models.IntegerField()
    itemssalevalue_sale = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='fruit_images/', null=True, blank=True)

    def __str__(self):
        return self.fruit_name

class Sale(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    total_value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Sale {self.id} by {self.user.username}"

class SaleItem(models.Model):
    DISCOUNT_CHOICES = [
        ('5%', '5%'),
        ('10%', '10%'),
        ('15%', '15%'),
        ('20%', '20%'),
        ('25%', '25%'),
    ]
    id = models.AutoField(primary_key=True)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    fruit = models.ForeignKey(Fruit, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unitary_value = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.CharField(max_length=10, choices=DISCOUNT_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"{self.quantity} x {self.fruit.fruit_name} (Sale {self.sale.id})"
