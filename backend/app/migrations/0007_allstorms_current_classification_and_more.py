# Generated by Django 4.2.19 on 2025-03-09 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_rename_date_yyyymmdd_allstorms_date_end_yyyymmdd_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='allstorms',
            name='current_classification',
            field=models.CharField(default='UNKNOWN', max_length=50),
        ),
        migrations.AddField(
            model_name='allstorms',
            name='highest_classification',
            field=models.CharField(default='UNKNOWN', max_length=50),
        ),
    ]
