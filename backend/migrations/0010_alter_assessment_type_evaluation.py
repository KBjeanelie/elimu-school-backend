# Generated by Django 4.1.5 on 2024-03-01 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_classroom_do_class'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='type_evaluation',
            field=models.CharField(choices=[('Devoir de classe', 'Devoir de classe'), ('Examen', 'Examen')], max_length=20, null=True),
        ),
    ]
