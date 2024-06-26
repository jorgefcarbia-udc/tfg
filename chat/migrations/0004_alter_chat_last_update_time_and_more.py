# Generated by Django 5.0.1 on 2024-01-16 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_chat_last_update_time_alter_user_last_login_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='last_update_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_login_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
