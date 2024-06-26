# Generated by Django 4.2.6 on 2024-01-19 15:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spons_app', '0003_alter_event_brochure_alter_event_expected_reg_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sponsorship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of_sponsorship', models.CharField(max_length=254)),
                ('money_donated', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spons_app.company')),
            ],
        ),
        migrations.RemoveField(
            model_name='event',
            name='money_raised',
        ),
        migrations.AddField(
            model_name='event',
            name='description',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.DeleteModel(
            name='Sponsors',
        ),
        migrations.AddField(
            model_name='sponsorship',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spons_app.event'),
        ),
    ]
