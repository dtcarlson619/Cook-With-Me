# Generated by Django 2.2 on 2020-01-31 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cook_with_me_app', '0004_auto_20200130_2200'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='restaurant_manager',
            field=models.BooleanField(default=False),
        ),
    ]
