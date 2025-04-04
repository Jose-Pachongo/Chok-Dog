# Generated by Django 5.1.5 on 2025-04-02 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comida', '0052_alter_pedido_estado_alter_reserva_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='estado',
            field=models.CharField(choices=[('Pendiente', 'Pendiente'), ('Confirmado', 'Confirmado'), ('Enviado', 'Enviado'), ('Entregado', 'Entregado'), ('Cancelado', 'Cancelado')], default='Pendiente', max_length=20),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='estado',
            field=models.CharField(choices=[('Pendiente', 'Pendiente'), ('Confirmado', 'Confirmado'), ('Cancelado', 'Cancelado')], default='Pendiente', max_length=20),
        ),
    ]
