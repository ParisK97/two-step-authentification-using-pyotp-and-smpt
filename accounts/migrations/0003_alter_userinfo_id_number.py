# Generated by Django 5.0.6 on 2024-11-26 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_userinfo_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='id_number',
            field=models.CharField(max_length=13, unique=True),
        ),
    ]