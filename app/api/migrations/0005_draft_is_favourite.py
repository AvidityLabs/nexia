# Generated by Django 3.2.18 on 2023-05-31 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20230530_1916'),
    ]

    operations = [
        migrations.AddField(
            model_name='draft',
            name='is_favourite',
            field=models.BooleanField(default=False),
        ),
    ]
