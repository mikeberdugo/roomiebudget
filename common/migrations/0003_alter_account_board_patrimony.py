# Generated by Django 5.0.4 on 2024-07-03 15:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_remove_board_linked_users_permit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='board',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.board'),
        ),
        migrations.CreateModel(
            name='Patrimony',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency', models.CharField(max_length=3)),
                ('patrimony_type', models.CharField(max_length=50)),
                ('type_dos', models.IntegerField()),
                ('status', models.CharField(max_length=20)),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.board')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
