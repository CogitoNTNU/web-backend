# Generated by Django 5.0.1 on 2025-01-20 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0005_memberapplication_lead'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memberapplication',
            name='lead',
            field=models.BooleanField(default=False, help_text='Whether the applicant wants to be a project lead'),
        ),
    ]
