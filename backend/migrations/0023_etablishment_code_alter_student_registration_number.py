# Generated by Django 4.1.5 on 2024-03-30 07:10

import backend.models.gestion_ecole
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0022_remove_student_is_archive_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='etablishment',
            name='code',
            field=backend.models.gestion_ecole.UUID4Field(editable=False, max_length=10, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='registration_number',
            field=backend.models.gestion_ecole.ShortUUID4Field(editable=False, max_length=14, unique=True),
        ),
    ]
