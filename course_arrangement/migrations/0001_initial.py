# Generated by Django 2.0.5 on 2018-06-10 01:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('college', models.CharField(max_length=255)),
                ('floor', models.IntegerField()),
                ('capacity', models.IntegerField()),
                ('room_id', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('total_period_number', models.IntegerField()),
                ('total_week_number', models.IntegerField()),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course_arrangement.ClassRoom')),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lectures', to='course_arrangement.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.IntegerField()),
                ('day', models.IntegerField()),
                ('section', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Requirement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('favorite', models.IntegerField(choices=[(5, 5), (1, 1), (2, 2), (-10, -10), (4, 4), (3, 3)], default=2)),
                ('lecture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course_arrangement.Lecture')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='period',
            unique_together={('week', 'day', 'section')},
        ),
        migrations.AddField(
            model_name='lecture',
            name='period',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course_arrangement.Period'),
        ),
        migrations.AlterUniqueTogether(
            name='lecture',
            unique_together={('classroom', 'period')},
        ),
    ]