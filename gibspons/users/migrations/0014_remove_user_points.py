# Generated by Django 5.0.1 on 2024-04-17 10:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_user_profile_pic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='points',
        ),
    ]
