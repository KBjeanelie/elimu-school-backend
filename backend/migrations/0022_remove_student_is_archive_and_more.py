# Generated by Django 4.1.5 on 2024-03-28 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0021_student_is_archive'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='is_archive',
        ),
        migrations.AddField(
            model_name='studentclassroom',
            name='is_archive',
            field=models.BooleanField(default=False),
        ),
    ]