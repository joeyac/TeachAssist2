# Generated by Django 2.0.5 on 2018-06-16 21:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='graproject',
            name='create_year',
        ),
        migrations.RemoveField(
            model_name='graproject',
            name='end_year',
        ),
    ]
