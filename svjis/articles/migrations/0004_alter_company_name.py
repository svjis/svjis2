# Generated by Django 5.0.6 on 2024-07-05 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_usefullink'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(blank=True, max_length=100, verbose_name='Name'),
        ),
    ]