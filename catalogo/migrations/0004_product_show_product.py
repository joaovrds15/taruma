# Generated by Django 3.1 on 2023-05-06 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0003_auto_20230421_1748'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='show_product',
            field=models.BooleanField(default=True),
        ),
    ]
