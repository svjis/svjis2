# Generated by Django 5.1.5 on 2025-01-19 11:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_alter_company_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='articlecomment',
            options={'ordering': ['id'], 'permissions': (('svjis_add_article_comment', 'Can add Article comment'),)},
        ),
    ]
