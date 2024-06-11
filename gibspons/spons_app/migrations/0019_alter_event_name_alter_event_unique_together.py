# Generated by Django 5.0.1 on 2024-06-11 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spons_app', '0018_sponsorship_remarks'),
        ('users', '0015_otp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterUniqueTogether(
            name='event',
            unique_together={('name', 'organisation', 'start_date')},
        ),
    ]
