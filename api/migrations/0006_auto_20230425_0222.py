# Generated by Django 3.2.18 on 2023-04-24 23:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20230425_0019'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='user_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='username',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='tokenusage',
            name='pricing_plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.pricingplan'),
        ),
        migrations.AlterField(
            model_name='tokenusage',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
