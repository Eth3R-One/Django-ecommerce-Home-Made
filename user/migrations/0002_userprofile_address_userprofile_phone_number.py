# Generated by Django 4.1.4 on 2023-06-10 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='address',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Address'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(blank=True, default='', max_length=20, null=True, verbose_name='Phone Number'),
        ),
    ]