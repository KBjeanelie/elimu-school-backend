# Generated by Django 4.1.5 on 2024-03-05 12:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0017_parentdocument'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.parent'),
        ),
    ]
