# Generated by Django 5.0.1 on 2024-04-25 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spons_app', '0016_leaderboard'),
        ('users', '0014_remove_user_points'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='company',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='company',
            name='website',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='poc',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='poc',
            name='linkedin',
            field=models.URLField(null=True),
        ),
        migrations.AlterUniqueTogether(
            name='company',
            unique_together={('name', 'website', 'organisation', 'linkedin')},
        ),
    ]