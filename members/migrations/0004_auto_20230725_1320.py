# Generated by Django 3.2.7 on 2023-07-25 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0003_auto_20230725_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=50, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='member',
            name='linkedIn',
            field=models.URLField(blank=True, default='', verbose_name='LinkedIn'),
        ),
    ]
