# Generated by Django 4.2.7 on 2024-07-10 05:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apiserver', '0004_cususer_profile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cususer',
            old_name='profile',
            new_name='profile_image',
        ),
    ]
