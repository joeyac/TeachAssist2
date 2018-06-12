# Generated by Django 2.0.5 on 2018-06-10 20:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course_arrangement', '0002_auto_20180610_0225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='course',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lectures', to='course_arrangement.Course'),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='favorite',
            field=models.IntegerField(choices=[(-10, 'REJECT'), (2, 'MEDIOCRE'), (3, 'ACCEPT'), (5, 'MOST'), (1, 'LEAST'), (4, 'SECOND')], default=2),
        ),
    ]