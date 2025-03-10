# Generated by Django 5.0.1 on 2024-03-05 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0002_memberapplication_member_github'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.AlterModelOptions(
            name='member',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='memberapplication',
            name='about',
            field=models.TextField(blank=True, help_text="Applicant's main application"),
        ),
        migrations.RemoveField(
            model_name='member',
            name='category',
        ),
        migrations.AlterField(
            model_name='member',
            name='email',
            field=models.EmailField(blank=True, default='', help_text=' The email of the member', max_length=50, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='member',
            name='github',
            field=models.URLField(blank=True, default='', help_text=" The link of the member's GitHub profile", verbose_name='GitHub'),
        ),
        migrations.AlterField(
            model_name='member',
            name='image',
            field=models.ImageField(blank=True, help_text=' The image of the member', null=True, upload_to='images/', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='member',
            name='linkedIn',
            field=models.URLField(blank=True, default='', help_text="The link of the member's LinkedIn profile", verbose_name='LinkedIn'),
        ),
        migrations.AlterField(
            model_name='member',
            name='name',
            field=models.CharField(blank=True, default='', help_text=' The full name of the member', max_length=30, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='member',
            name='order',
            field=models.IntegerField(blank=True, default=0, help_text=' The order of the member in the list to be displayed on the frontend', primary_key=True, serialize=False, verbose_name='Order'),
        ),
        migrations.AlterField(
            model_name='member',
            name='title',
            field=models.CharField(blank=True, default='', help_text=" The title of the member, like 'CEO' or 'Team Lead'", max_length=30, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='memberapplication',
            name='date_of_application',
            field=models.DateTimeField(auto_now_add=True, help_text='The date and time the application was sent'),
        ),
        migrations.AlterField(
            model_name='memberapplication',
            name='email',
            field=models.EmailField(help_text="Applicant's email address", max_length=254),
        ),
        migrations.AlterField(
            model_name='memberapplication',
            name='first_name',
            field=models.CharField(help_text="Applicant's first name", max_length=100),
        ),
        migrations.AlterField(
            model_name='memberapplication',
            name='last_name',
            field=models.CharField(help_text="Applicant's last name", max_length=100),
        ),
        migrations.AlterField(
            model_name='memberapplication',
            name='phone_number',
            field=models.CharField(help_text="Applicant's phone number", max_length=15),
        ),
        migrations.CreateModel(
            name='ProjectDescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='images/')),
                ('hours_a_week', models.IntegerField()),
                ('leaders', models.ManyToManyField(to='team.member')),
            ],
        ),
        migrations.AddField(
            model_name='member',
            name='category',
            field=models.ManyToManyField(to='team.membercategory'),
        ),
    ]
