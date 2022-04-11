# Generated by Django 4.0.3 on 2022-03-29 01:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cdl_number', models.CharField(blank=True, max_length=20)),
                ('vehicle_id', models.IntegerField(blank=True, null=True)),
                ('co_driver_id', models.IntegerField(blank=True, null=True)),
                ('app_version', models.CharField(blank=True, max_length=5)),
                ('notes', models.CharField(blank=True, max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loc_name', models.CharField(max_length=50)),
                ('lat', models.DecimalField(decimal_places=6, max_digits=9)),
                ('lng', models.DecimalField(decimal_places=6, max_digits=9)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('unit_number', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('model', models.CharField(blank=True, max_length=20, null=True)),
                ('vin_number', models.CharField(blank=True, max_length=20, null=True)),
                ('is_active', models.BooleanField(default=1)),
                ('notes', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_code', models.SmallIntegerField(default=0)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('loc_name', models.CharField(blank=True, max_length=50, null=True)),
                ('lat', models.DecimalField(decimal_places=6, max_digits=9, null=True)),
                ('lng', models.DecimalField(decimal_places=6, max_digits=9, null=True)),
                ('odometer', models.IntegerField(null=True)),
                ('eng_hours', models.DecimalField(decimal_places=1, max_digits=6, null=True)),
                ('notes', models.CharField(blank=True, max_length=20, null=True)),
                ('document', models.CharField(blank=True, max_length=20, null=True)),
                ('trailer', models.CharField(blank=True, max_length=20, null=True)),
                ('driver_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eld.driver')),
                ('vehicle_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='eld.vehicle')),
            ],
        ),
    ]