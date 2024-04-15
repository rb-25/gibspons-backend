# Generated by Django 5.0.1 on 2024-04-15 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spons_app', '0013_alter_company_options_alter_event_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsorship',
            name='status',
            field=models.CharField(choices=[('Not Contacted', 'Not Contacted'), ('No Reply', 'No Reply'), ('In Progress', 'In Progress'), ('Rejected', 'Rejected'), ('Accepted', 'Accepted')], default='Not Contacted', max_length=20),
        ),
    ]