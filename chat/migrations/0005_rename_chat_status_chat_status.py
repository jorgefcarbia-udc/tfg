# Generated by Django 5.0.1 on 2024-01-17 09:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_alter_chat_last_update_time_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chat',
            old_name='chat_status',
            new_name='status',
        ),
    ]
