# Generated by Django 4.0.4 on 2022-05-06 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0002_rename_restaurant_restaurant_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurants.restaurant'),
        ),
    ]
