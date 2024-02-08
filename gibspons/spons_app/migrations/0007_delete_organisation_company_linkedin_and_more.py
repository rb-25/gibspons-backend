# Generated by Django 5.0.1 on 2024-02-05 18:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spons_app', '0006_organisation'),
        ('users', '0008_organisation_industry_organisation_location_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Organisation',
        ),
        migrations.AddField(
            model_name='company',
            name='linkedin',
            field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='organisation',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.organisation'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company',
            name='updated_at',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='event',
            name='organisation',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.organisation'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='poc',
            name='designation',
            field=models.CharField(default='Worker', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sponsorship',
            name='additional',
            field=models.CharField(default='Inkind'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='company',
            name='status',
            field=models.CharField(choices=[('No Reply', 'No Reply'), ('In Progress', 'In Progress'), ('Rejected', 'Rejected'), ('Accepted', 'Accepted')], default='No Reply', max_length=20),
        ),
    ]
