# Generated by Django 2.0.5 on 2018-06-16 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_arrangement', '0004_auto_20180615_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requirement',
            name='favorite',
            field=models.IntegerField(choices=[(3, 'ACCEPT'), (2, 'MEDIOCRE'), (1, 'LEAST'), (5, 'MOST'), (4, 'SECOND'), (-10, 'REJECT')], default=2),
        ),
    ]
