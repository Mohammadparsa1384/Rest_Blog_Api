# Generated by Django 4.2.7 on 2025-06-18 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'category', 'verbose_name_plural': 'categories'},
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
