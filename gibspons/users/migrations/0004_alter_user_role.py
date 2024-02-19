# Generated by Django 4.2.6 on 2024-01-19 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_managers_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('user', 'User'), ('owner', 'Owner'), ('admin', 'Admin')], max_length=20),
        ),
    ]