# Generated by Django 4.1.5 on 2024-02-27 12:57

import backend.models.gestion_ecole
import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicYear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=50)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ClassRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('types', models.CharField(choices=[('Primaire', 'Primaire'), ('College', 'College'), ('Lycée', 'Lycée')], max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='DocumentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('status', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Etablishment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('tel', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=100)),
                ('social_address', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(blank=True, max_length=200, null=True)),
                ('bulletin_foot', models.CharField(blank=True, max_length=50, null=True)),
                ('currency', models.CharField(blank=True, choices=[('F CFA', 'F CFA')], max_length=50, null=True)),
                ('système', models.CharField(blank=True, choices=[('Congolais', 'Congolais')], max_length=50, null=True)),
                ('status_fees', models.CharField(blank=True, choices=[('Activé', 'Activé'), ('Desactivé', 'Desactivé')], max_length=50, null=True)),
                ('subscription_fees', models.IntegerField(blank=True, default=1000, null=True)),
                ('month', models.IntegerField(blank=True, default=9, null=True)),
                ('re_registration_fees', models.IntegerField(blank=True, default=800, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GroupSubject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.etablishment')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.CharField(max_length=50, unique=True)),
                ('invoice_date', models.DateField(auto_now=True)),
                ('amount', models.FloatField(default=0)),
                ('schooling_of', models.CharField(choices=[('Janvier', 'Janvier'), ('Février', 'Février'), ('Mars', 'Mars'), ('Avril', 'Avril'), ('Mai', 'Mai'), ('Juin', 'Juin'), ('Juillet', 'Juillet'), ('Août', 'Août'), ('Septembre', 'Septembre'), ('Octobre', 'Octobre'), ('Novembre', 'Novembre'), ('Décembre', 'Décembre')], max_length=10)),
                ('invoice_status', models.CharField(blank=True, choices=[('Entièrement payé', 'Entièrement payé'), ('Non payé', 'Non payé'), ('Avance', 'Avance')], max_length=20)),
                ('is_repayment', models.BooleanField(default=False)),
                ('comment', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('academic_year', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.academicyear')),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.classroom')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('default_amount', models.IntegerField(default=0)),
                ('defaut_quantity', models.IntegerField(default=1)),
                ('is_active', models.BooleanField(default=True)),
                ('analytic_code', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.etablishment')),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=50)),
                ('fees', models.IntegerField(default=1000)),
                ('cycles', models.CharField(choices=[('Primaire', 'Primaire'), ('College', 'College'), ('College Technique industrielle', ' College technique industrielle'), ('Lycée général', 'Lycée général'), ('Lycée technique commerciale', 'Lycée technique commerciale'), ('Lycée technique industrielle', 'Lycée technique industrielle')], max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ManagementProfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lastname', models.CharField(blank=True, max_length=50)),
                ('firstname', models.CharField(blank=True, max_length=50)),
                ('address', models.CharField(blank=True, max_length=50)),
                ('tel', models.CharField(blank=True, max_length=20)),
                ('city', models.CharField(blank=True, choices=[('pointe_noire', 'Pointe Noire'), ('brazzaville', 'Brazzaville')], max_length=17)),
                ('sex', models.CharField(blank=True, choices=[('masculin', 'Masculin'), ('feminin', 'Féminin')], max_length=10)),
                ('email', models.CharField(blank=True, max_length=120, null=True, unique=True)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='managements_images')),
                ('bio', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_number', backend.models.gestion_ecole.ShortUUID4Field(editable=False, max_length=10, unique=True)),
                ('lastname', models.CharField(blank=True, max_length=50, null=True)),
                ('firstname', models.CharField(blank=True, max_length=50, null=True)),
                ('address', models.CharField(blank=True, max_length=50, null=True)),
                ('tel', models.CharField(blank=True, max_length=20)),
                ('city', models.CharField(blank=True, choices=[('pointe_noire', 'Pointe Noire'), ('brazzaville', 'Brazzaville')], max_length=17)),
                ('sex', models.CharField(blank=True, choices=[('masculin', 'Masculin'), ('feminin', 'Féminin')], max_length=10)),
                ('email', models.CharField(blank=True, max_length=120, null=True, unique=True)),
                ('bithday', models.DateField(blank=True, null=True)),
                ('nationality', models.CharField(blank=True, max_length=20)),
                ('blood_type', models.CharField(blank=True, choices=[('O+', 'O+'), ('O-', 'O-'), ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-')], max_length=5, null=True)),
                ('birthday_place', models.CharField(blank=True, max_length=100, null=True)),
                ('allergy', models.CharField(blank=True, max_length=255, null=True)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='student_images')),
                ('status', models.BooleanField(default=False)),
                ('is_valid', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lastname', models.CharField(blank=True, max_length=50)),
                ('firstname', models.CharField(blank=True, max_length=50)),
                ('address', models.CharField(blank=True, max_length=50)),
                ('tel', models.CharField(blank=True, max_length=20)),
                ('city', models.CharField(blank=True, choices=[('pointe_noire', 'Pointe Noire'), ('brazzaville', 'Brazzaville')], max_length=17)),
                ('sex', models.CharField(blank=True, choices=[('masculin', 'Masculin'), ('feminin', 'Féminin')], max_length=10)),
                ('bithday', models.DateField(blank=True, null=True)),
                ('nationality', models.CharField(blank=True, max_length=20)),
                ('email', models.CharField(blank=True, max_length=120, unique=True)),
                ('status', models.CharField(blank=True, max_length=20)),
                ('last_diploma', models.CharField(blank=True, choices=[('Doctorat', 'Doctorat'), ('Master', 'Master'), ('Licence', 'Licence'), ('DUT', 'DUT'), ('Baccalauréat', 'Baccalauréat')], max_length=20)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='teacher_images')),
                ('type_of_counter', models.CharField(blank=True, max_length=20)),
                ('start_of_contrat', models.DateField(blank=True, null=True)),
                ('end_of_contrat', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.etablishment')),
            ],
        ),
        migrations.CreateModel(
            name='TypeOfEvaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('school', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.etablishment')),
            ],
        ),
        migrations.CreateModel(
            name='TeacherDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('file', models.FileField(upload_to='teacher_documents')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('document_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.documenttype')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=50)),
                ('type', models.CharField(choices=[('Obligatoire', 'Obligatoire'), ('Secondaire', 'Secondaire')], max_length=12)),
                ('possible_evaluation', models.BooleanField(default=True)),
                ('possible_averaging', models.BooleanField(default=True)),
                ('coefficient', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.level')),
                ('subject_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.groupsubject')),
                ('teacher_in_charge', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='StudentDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('file', models.FileField(upload_to='student_documents')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('document_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.documenttype')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.student')),
            ],
        ),
        migrations.CreateModel(
            name='StudentClassroom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_registered', models.BooleanField(default=False)),
                ('is_valid', models.BooleanField(default=False)),
                ('is_next', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('academic_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.academicyear')),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.classroom')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.student')),
            ],
        ),
        migrations.CreateModel(
            name='Spend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=0)),
                ('comment', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('academic_year', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.academicyear')),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.item')),
            ],
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.etablishment')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_hours', models.CharField(choices=[('07h', '07h'), ('08h', '08h'), ('09h', '09h'), ('10h', '10h'), ('11h', '11h'), ('12h', '12h'), ('13h', '13h'), ('14h', '14h'), ('15h', '15h'), ('16h', '16h'), ('17h', '17h')], max_length=15)),
                ('end_hours', models.CharField(choices=[('07h', '07h'), ('08h', '08h'), ('09h', '09h'), ('10h', '10h'), ('11h', '11h'), ('12h', '12h'), ('13h', '13h'), ('14h', '14h'), ('15h', '15h'), ('16h', '16h'), ('17h', '17h')], max_length=15)),
                ('day', models.CharField(choices=[('lundi', 'Lundi'), ('mardi', 'Mardi'), ('mercredi', 'Mercredi'), ('jeudi', 'Jeudi'), ('vendredi', 'Vendredi'), ('samedi', 'Samedi'), ('dimanche', 'Dimanche')], max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.classroom')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.subject')),
            ],
        ),
        migrations.CreateModel(
            name='SanctionAppreciationType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.etablishment')),
            ],
        ),
        migrations.CreateModel(
            name='SanctionAppreciation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('academic_year', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.academicyear')),
                ('classroom', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.classroom')),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.student')),
                ('subject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.subject')),
                ('type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.sanctionappreciationtype')),
            ],
        ),
        migrations.CreateModel(
            name='ReportCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('average', models.FloatField(default=10)),
                ('file', models.FileField(upload_to='releves_notes')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('academic_year', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='backend.academicyear')),
                ('career', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='backend.classroom')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='backend.series')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.student')),
            ],
        ),
        migrations.CreateModel(
            name='Repayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('repayment_method', models.CharField(choices=[('Par chèque', 'Par chèque'), ('En espèce', 'En espèce')], max_length=20)),
                ('amount', models.FloatField(default=0)),
                ('repayment_date', models.DateField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
                ('comment', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('academic_year', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.academicyear')),
                ('invoice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.invoice')),
            ],
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True)),
                ('file', models.FileField(blank=True, upload_to='programmes')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.level')),
                ('person_in_charge', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.teacher')),
            ],
        ),
        migrations.AddField(
            model_name='level',
            name='principal_teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.teacher'),
        ),
        migrations.AddField(
            model_name='level',
            name='serie',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.series'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.item'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.student'),
        ),
        migrations.CreateModel(
            name='Information',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('content', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('file', models.FileField(blank=True, upload_to='info_files')),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.etablishment')),
            ],
        ),
        migrations.CreateModel(
            name='FinancialCommitment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_fees', models.IntegerField()),
                ('send_date', models.DateTimeField(blank=True, null=True)),
                ('is_send', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('academic_year', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.academicyear')),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.student')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('content', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('status', models.BooleanField(default=True)),
                ('file', models.FileField(blank=True, upload_to='events_files/')),
                ('photo', models.ImageField(blank=True, upload_to='events_image/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.etablishment')),
            ],
        ),
        migrations.CreateModel(
            name='eBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('photo_cover', models.ImageField(upload_to='images_ebook')),
                ('attachement', models.FileField(upload_to='ebook_folder')),
                ('is_private', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.teacher')),
                ('level', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.level')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.etablishment')),
            ],
        ),
        migrations.AddField(
            model_name='documenttype',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.etablishment'),
        ),
        migrations.AddField(
            model_name='classroom',
            name='level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.level'),
        ),
        migrations.CreateModel(
            name='Assessment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.IntegerField(default=0)),
                ('is_publish', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('academic_year', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='backend.academicyear')),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='backend.classroom')),
                ('serie', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='backend.series')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.student')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='backend.subject')),
                ('type_evaluation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.typeofevaluation')),
            ],
        ),
        migrations.AddField(
            model_name='academicyear',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.etablishment'),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=255, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_admin_school', models.BooleanField(default=False)),
                ('is_manager', models.BooleanField(default=False)),
                ('is_accountant', models.BooleanField(default=False)),
                ('is_student', models.BooleanField(default=False)),
                ('is_teacher', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('management_profil', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.managementprofil')),
                ('school', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.etablishment')),
                ('student', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.student')),
                ('teacher', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.teacher')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
