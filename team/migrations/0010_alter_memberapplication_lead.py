# Generated by Django 5.0.1 on 2025-01-20 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0009_alter_memberapplication_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memberapplication',
            name='lead',
            field=models.BooleanField(blank=True, default=False, help_text='Whether the applicant wants to be a project lead'),
        ),
    ]
