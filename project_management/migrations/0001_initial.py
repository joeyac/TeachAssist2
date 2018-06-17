# Generated by Django 2.0.5 on 2018-06-16 13:05

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
            name='EduProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('create_year', models.DateField()),
                ('end_year', models.DateField()),
                ('pro_state', models.CharField(choices=[('unconfirmed', 'UNCONFIRMED'), ('terminated', 'TERMINATED'), ('terminate_unconfirmed', 'TERMINATE_UNCONFIRMED'), ('postponed', 'POSTPONED'), ('postpone_unconfirmed', 'POSTPONE_UNCONFIRMED'), ('midterm_passed', 'MIDTERM_PASSED'), ('midterm_checking', 'MIDTERM_CHECKING'), ('final_checking', 'FINAL_CHEKING'), ('done', 'DONE'), ('apply_passed', 'APPLY_PASSED')], default='unconfirmed', max_length=10)),
                ('pro_level', models.CharField(choices=[('院级', 'COLLEGE'), ('市级推荐级', 'MUNICIPALPROMOTED'), ('国家推荐级', 'NATIONALPROMOTED')], default='院级', max_length=10)),
                ('members', models.CharField(max_length=500)),
                ('file1', models.FilePathField()),
                ('file2', models.FilePathField(null=True)),
                ('file3', models.FilePathField(null=True)),
                ('file4', models.FilePathField(null=True)),
                ('pro_name', models.CharField(max_length=100)),
                ('introduction', models.CharField(max_length=2000)),
                ('person_in_charge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='PIC_edu', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GraProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('create_year', models.DateField()),
                ('end_year', models.DateField()),
                ('file1', models.FilePathField(null=True)),
                ('file2', models.FilePathField(null=True)),
                ('file3', models.FilePathField(null=True)),
                ('file4', models.FilePathField(null=True)),
                ('file5', models.FilePathField(null=True)),
                ('pro_name', models.CharField(max_length=100)),
                ('introduction', models.CharField(max_length=2000)),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student_gra', to=settings.AUTH_USER_MODEL)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_gra', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SRTPProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('create_year', models.DateField()),
                ('end_year', models.DateField()),
                ('pro_state', models.CharField(choices=[('unconfirmed', 'UNCONFIRMED'), ('terminated', 'TERMINATED'), ('terminate_unconfirmed', 'TERMINATE_UNCONFIRMED'), ('postponed', 'POSTPONED'), ('postpone_unconfirmed', 'POSTPONE_UNCONFIRMED'), ('midterm_passed', 'MIDTERM_PASSED'), ('midterm_checking', 'MIDTERM_CHECKING'), ('final_checking', 'FINAL_CHEKING'), ('done', 'DONE'), ('apply_passed', 'APPLY_PASSED')], default='unconfirmed', max_length=10)),
                ('pro_level', models.CharField(choices=[('院级', 'COLLEGE'), ('市级推荐级', 'MUNICIPALPROMOTED'), ('国家推荐级', 'NATIONALPROMOTED')], default='院级', max_length=10)),
                ('members', models.CharField(max_length=500)),
                ('instructor', models.CharField(max_length=32)),
                ('file1', models.FilePathField(null=True)),
                ('file2', models.FilePathField(null=True)),
                ('file3', models.FilePathField(null=True)),
                ('file4', models.FilePathField(null=True)),
                ('pro_name', models.CharField(max_length=100)),
                ('introduction', models.CharField(max_length=2000)),
                ('person_in_charge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='PIC_srtp', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
