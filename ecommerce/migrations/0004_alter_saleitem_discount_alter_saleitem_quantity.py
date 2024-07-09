# Generated by Django 5.0.6 on 2024-07-07 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0003_alter_saleitem_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saleitem',
            name='discount',
            field=models.CharField(choices=[('5%', '5%'), ('10%', '10%'), ('15%', '15%'), ('20%', '20%'), ('25%', '25%')], max_length=10),
        ),
        migrations.AlterField(
            model_name='saleitem',
            name='quantity',
            field=models.IntegerField(),
        ),
    ]
