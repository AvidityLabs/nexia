# Generated by Django 3.2.18 on 2023-04-20 03:24

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PricingPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.CharField(blank=True, max_length=100, null=True)),
                ('name', models.CharField(max_length=50)),
                ('api_request_limit', models.IntegerField(default=0)),
                ('rate_limit', models.IntegerField(default=0)),
                ('token_limit', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='user',
            name='total_tokens_used',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.CharField(blank=True, max_length=100, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('pricing_plan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.pricingplan')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='tokenusage',
            name='pricing_plan',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.pricingplan'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='subscription',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.subscription'),
        ),
    ]