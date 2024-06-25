# Generated by Django 5.0.6 on 2024-06-25 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_profile_created_on_remove_profile_modified_on'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='modified_by',
        ),
        migrations.AddField(
            model_name='profile',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='modified_on',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
