# Generated by Django 2.0.5 on 2018-06-14 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('secretary', 'SECRETARY'), ('teacher', 'TEACHER'), ('student', 'STUDENT')], default='student', max_length=10),
        ),
    ]
