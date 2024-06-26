# Generated by Django 5.0.1 on 2024-04-25 07:03

import django.db.models.deletion
import users.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_remove_user_points'),
    ]

    operations = [
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=6, validators=[users.models.OTP.validate_otp_value])),
                ('expiry_date', models.DateTimeField(default=users.models.get_expiry_date)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='otp', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'OTP',
                'verbose_name_plural': 'OTPs',
            },
        ),
    ]
