# Generated by Django 5.0.6 on 2024-05-16 20:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='vacation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='api.vacationsmodel'),
        ),
    ]