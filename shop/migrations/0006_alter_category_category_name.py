# Generated by Django 5.1.2 on 2024-10-15 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_alter_picture_cover_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_name',
            field=models.CharField(blank=True, max_length=255, unique=True, verbose_name='Категория'),
        ),
    ]