# Generated by Django 2.0.5 on 2018-06-12 18:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EduProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('pro_state', models.CharField(choices=[('done', 'DONE'), ('postponed', 'POSTPONED'), ('running', 'RUNNING'), ('abandoned', 'ABANDONED')], default='running', max_length=10)),
                ('pro_level', models.CharField(choices=[('国家推荐级', 'NATIONALPROMOTED'), ('院级', 'COLLEGE'), ('市级推荐级', 'MUNICIPALPROMOTED')], default='院级', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='GraProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_time', models.DateTimeField(auto_now=True, null=True)),
                ('student', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student_gra', to=settings.AUTH_USER_MODEL)),
                ('teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teacher_gra', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SRTPProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('pro_state', models.CharField(choices=[('done', 'DONE'), ('postponed', 'POSTPONED'), ('running', 'RUNNING'), ('abandoned', 'ABANDONED')], default='running', max_length=10)),
                ('pro_level', models.CharField(choices=[('国家推荐级', 'NATIONALPROMOTED'), ('院级', 'COLLEGE'), ('市级推荐级', 'MUNICIPALPROMOTED')], default='院级', max_length=10)),
                ('students', models.ManyToManyField(related_name='students_srtp', to=settings.AUTH_USER_MODEL)),
                ('teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teacher_srtp', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
