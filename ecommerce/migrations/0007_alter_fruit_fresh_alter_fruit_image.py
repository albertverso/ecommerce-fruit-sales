# Generated by Django 5.0.6 on 2024-09-03 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0006_alter_saleitem_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fruit',
            name='fresh',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='fruit',
            name='image',
            field=models.TextField(blank=True, null=True),
        ),
    ]
