# Generated by Django 3.2.7 on 2023-07-28 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='newProject',
            fields=[
                ('title', models.CharField(blank=True, default='', max_length=30, primary_key=True, serialize=False)),
                ('desc', models.CharField(blank=True, default='', max_length=200)),
            ],
        ),
    ]
