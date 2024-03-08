# Generated by Django 5.0.2 on 2024-03-08 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_alter_article_options_alter_articlecomment_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationSetup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=50, verbose_name='Key')),
                ('value', models.CharField(max_length=1000, verbose_name='Value')),
            ],
        ),
        migrations.CreateModel(
            name='Buliding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=50, verbose_name='Address')),
                ('city', models.CharField(max_length=50, verbose_name='City')),
                ('post_code', models.CharField(max_length=10, verbose_name='Post code')),
                ('registration_no', models.CharField(max_length=50, verbose_name='Registration no.')),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('address', models.CharField(max_length=50, verbose_name='Address')),
                ('city', models.CharField(max_length=50, verbose_name='City')),
                ('post_code', models.CharField(max_length=10, verbose_name='Post code')),
                ('phone', models.CharField(max_length=30, verbose_name='Phone')),
                ('email', models.CharField(max_length=50, verbose_name='E-Mail')),
                ('registration_no', models.CharField(max_length=20, verbose_name='Registration no.')),
                ('vat_registration_no', models.CharField(max_length=20, verbose_name='VAT Registration no.')),
                ('internet_domain', models.CharField(max_length=50, verbose_name='VAT Registration no.')),
            ],
        ),
        migrations.CreateModel(
            name='MessageQueue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=50, verbose_name='E-Mail')),
                ('subject', models.CharField(max_length=100, verbose_name='Subject')),
                ('body', models.TextField(verbose_name='Body')),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('sending_time', models.DateTimeField(null=True)),
                ('status', models.SmallIntegerField()),
            ],
        ),
    ]
