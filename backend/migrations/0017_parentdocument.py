# Generated by Django 4.1.5 on 2024-03-05 11:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0016_alter_parent_picture_one'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParentDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('file', models.FileField(upload_to='famille_documents')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('document_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.documenttype')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.parent')),
            ],
        ),
    ]
