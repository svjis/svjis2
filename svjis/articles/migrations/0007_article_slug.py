# Generated by Django 5.0.3 on 2024-03-20 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0006_survey_surveyoption_surveyanswerlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='slug',
            field=models.CharField(default='', max_length=100),
        ),
    ]
