# Generated by Django 5.0.1 on 2024-05-01 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spons_app', '0017_alter_company_unique_together_alter_company_website_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsorship',
            name='remarks',
            field=models.CharField(max_length=500, null=True),
        ),
    ]