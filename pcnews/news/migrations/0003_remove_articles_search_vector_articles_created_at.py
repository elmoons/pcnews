# Generated by Django 4.2.7 on 2024-01-12 06:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_alter_articles_options_articles_search_vector'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articles',
            name='search_vector',
        ),
        migrations.AddField(
            model_name='articles',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
