# Generated by Django 3.2.18 on 2023-10-05 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='document_type',
            field=models.CharField(blank=True, choices=[('pdf', 'PDF'), ('doc', 'DOC'), ('csv', 'CSV'), ('html', 'HTML')], max_length=10, null=True),
        ),
    ]
