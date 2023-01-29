# Generated by Django 4.1.5 on 2023-01-28 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flightNumber', models.CharField(max_length=4)),
                ('date', models.CharField(max_length=10)),
                ('checkInTime', models.CharField(max_length=15)),
                ('tsa', models.CharField(max_length=15)),
                ('walkingTime', models.CharField(max_length=15)),
            ],
        ),
    ]
