# Generated by Django 4.1.5 on 2024-02-28 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_remove_assessment_serie_assessment_period_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='classroom',
            name='do_class',
            field=models.CharField(choices=[('Le matin', 'Le matin'), ('Après midi', 'Après midi'), ('Plein temps', 'Plein temps')], max_length=11, null=True),
        ),
    ]
