# Generated by Django 3.2.18 on 2023-04-24 00:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.CharField(default=uuid.uuid4, max_length=100, primary_key=True, serialize=False, unique=True)),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True)),
                ('username', models.CharField(db_index=True, max_length=255, unique=True)),
                ('is_developer', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('api_key', models.CharField(blank=True, max_length=100, null=True)),
                ('total_tokens_used', models.IntegerField(default=0)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EmotionAnalysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True)),
                ('anger_score', models.FloatField(blank=True, null=True)),
                ('disgust_score', models.FloatField(blank=True, null=True)),
                ('fear_score', models.FloatField(blank=True, null=True)),
                ('joy_score', models.FloatField(blank=True, null=True)),
                ('neutral_score', models.FloatField(blank=True, null=True)),
                ('sadness_score', models.FloatField(blank=True, null=True)),
                ('surprise_score', models.FloatField(blank=True, null=True)),
                ('analyzed_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PricingPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.CharField(blank=True, max_length=100, null=True)),
                ('name', models.CharField(blank=True, choices=[('basic', 'Basic'), ('pro', 'Pro'), ('ultra', 'Ultra'), ('mega', 'Mega'), ('custom', 'Custom')], max_length=50, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('features', models.TextField(blank=True, null=True)),
                ('monthly_price', models.DecimalField(decimal_places=2, default='0.00', max_digits=8)),
                ('monthly_character_limit', models.IntegerField(default=0)),
                ('rate_limit', models.IntegerField(default=0)),
                ('data_storage_limit', models.IntegerField(default=0)),
                ('additional_character_charge', models.DecimalField(decimal_places=4, default='0.00', max_digits=8)),
                ('currency', models.CharField(default='USD', max_length=3)),
            ],
            options={
                'ordering': ['-created_at', '-updated_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SentimentAnalysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True)),
                ('positive', models.FloatField(blank=True, null=True)),
                ('analyzed_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TokenUsage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prompt_tokens_used', models.IntegerField(default=0)),
                ('completion_tokens_used', models.IntegerField(default=0)),
                ('total_tokens_used', models.IntegerField(default=0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('pricing_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.pricingplan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
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
                'ordering': ['-created_at', '-updated_at'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='user',
            name='subscription',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.subscription'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
