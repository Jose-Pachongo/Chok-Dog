# Generated by Django 5.1.5 on 2025-02-24 21:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comida', '0002_mesa_reserva_mesa'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reserva',
            name='mesa',
        ),
        migrations.DeleteModel(
            name='Mesa',
        ),
    ]
