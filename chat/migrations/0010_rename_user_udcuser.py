# Generated by Django 5.0.1 on 2024-05-27 11:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0009_context_title'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='UDCUser',
        ),
    ]
