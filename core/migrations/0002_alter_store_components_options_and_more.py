# Generated by Django 4.1.4 on 2023-05-25 18:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='store_components',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AddField(
            model_name='store_components',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='store_components',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
