# Generated by Django 5.1.3 on 2024-11-27 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0002_rename_user_profile_username_profile_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='email',
            field=models.EmailField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='profile',
            name='password',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]
