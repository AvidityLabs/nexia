# Generated by Django 3.2.18 on 2023-06-08 23:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_user_uid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usecase',
            name='category',
        ),
        migrations.DeleteModel(
            name='Draft',
        ),
        migrations.DeleteModel(
            name='UseCase',
        ),
        migrations.DeleteModel(
            name='UseCaseCategory',
        ),
    ]
