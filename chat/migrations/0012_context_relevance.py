# Generated by Django 5.0.1 on 2024-05-28 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0011_udcuser_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='context',
            name='relevance',
            field=models.FloatField(default=0),
        ),
    ]
