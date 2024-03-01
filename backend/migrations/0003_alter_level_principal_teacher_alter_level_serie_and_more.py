# Generated by Django 4.1.5 on 2024-02-27 15:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_alter_subject_subject_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='level',
            name='principal_teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.teacher'),
        ),
        migrations.AlterField(
            model_name='level',
            name='serie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.series'),
        ),
        migrations.AlterField(
            model_name='sanctionappreciation',
            name='academic_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.academicyear'),
        ),
        migrations.AlterField(
            model_name='sanctionappreciation',
            name='classroom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.classroom'),
        ),
        migrations.AlterField(
            model_name='sanctionappreciation',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.student'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='subject_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.groupsubject'),
        ),
    ]