from django.conf.urls.static import static
from django.urls import path

from elimu_school import settings
from manager_dashboard.views.administration_view import EditProfileView, ProfileAppView, TypeDocumentDeleteView, TypeDocumentView, TypeEvaluationDeleteView, TypeEvaluationView, TypeSanctionDeleteView, TypeSanctionView, SettingAppView, get_last_document_type, get_last_sanction_type
from manager_dashboard.views.communication_view import AddEventView, AddInformationView, EditEventView, EditInformationView, EventDetail, EventView,  InformationDetail, InformationView
from manager_dashboard.views.comptes_view import AddDirectionAccount, AddStudentAccount, AddTeacherAccount, EditDirectionAccountView, EditStudentAccountView, EditTeacherAccountView, ListAllDirectionAccount, ListAllStudentAccount, ListAllTeacherAccount
from manager_dashboard.views.contenu_pedagogique_view import AddeBook, EditEbook, eBookView
from manager_dashboard.views.gestion_evaluation_view import AddAssessmentView, AssessmentView, AverageTableView, BulletinDetailView, EditAssessmentView, NoteTableView
from manager_dashboard.views.gestion_temps_view import AddScheduleView, ScheduleView
from manager_dashboard.views.gestion_universite_view import AcademicYearView, AddAcademicYearView, AddClassRoomView, AddLevelView, AddProgramView, AddSanctionView, AddStudentView, AddSubjectView, AddTeacherView, ClassRoomView, EditAcademicYearView, EditClassRoomView, EditLevelView, EditProgramView, EditSanctionView, EditStudentView, EditSubjectView, EditTeacherView, GroupSubjectView, LevelsView, ProgramView, SanctionAppreciationView, SeriesView, StudentDetailView, StudentsView, SubjectView, TeacherDetailView, TeacherView, TrombinoscopeView
from manager_dashboard.views.home_view import ManagerIndexView, NotAcademicYearFound
from manager_dashboard.views.statistique_view import AddNextLevelView, CloseAcademicYear, NextLevelView, ResultatAcademique, ReportCardView, AddReportCardView, EditReportCardView


app_name = 'manager_dashboard'
urlpatterns = [
    path(route='', view=ManagerIndexView.as_view(), name='index'),
    
    path(route='gestion_ecole/année-academiques/', view=AcademicYearView.as_view(), name='years'),
    path(route='gestion_ecole/année-academiques/ajouter/', view=AddAcademicYearView.as_view(), name='add_year'),
    path(route='gestion_ecole/année-academiques/<int:pk>/editer/', view=EditAcademicYearView.as_view(), name='edit_year'),
    path(route='gestion_ecole/année-academiques/<int:pk>/delete/', view=AcademicYearView.as_view(), name='delete_year'),
    
    path(route='gestion_ecole/series/', view=SeriesView.as_view(), name='series'),
    path(route='gestion_ecole/series/<int:pk>/delete/', view=SeriesView.as_view(), name='delete_series'),
    
    path(route='gestion_ecole/niveaux/', view=LevelsView.as_view(), name='levels'),
    path(route='gestion_ecole/niveaux/ajouter/', view=AddLevelView.as_view(), name='add_level'),
    path(route='gestion_ecole/niveaux/<int:pk>/editer/', view=EditLevelView.as_view(), name='edit_level'),
    path(route='gestion_ecole/niveaux/<int:pk>/delete/', view=LevelsView.as_view(), name='delete_level'),
    
    path(route='gestion_ecole/salle-de-classe/', view=ClassRoomView.as_view(), name='classrooms'),
    path(route='gestion_ecole/salle-de-classe/ajouter/', view=AddClassRoomView.as_view(), name='add_classroom'),
    path(route='gestion_ecole/salle-de-classe/<int:pk>/editer/', view=EditClassRoomView.as_view(), name='edit_classroom'),
    path(route='gestion_ecole/salle-de-classe/<int:pk>/delete/', view=ClassRoomView.as_view(), name='delete_classroom'),
    

    path(route='gestion_ecole/groupe-de-matières/', view=GroupSubjectView.as_view(), name='group_subjects'),
    path(route='gestion_ecole/groupe-de-matières/<int:pk>/delete/', view=GroupSubjectView.as_view(), name='delete_group_subjects'),
    
    path(route='gestion_ecole/matières/', view=SubjectView.as_view(), name='subjects'),
    path(route='gestion_ecole/matières/ajouter/', view=AddSubjectView.as_view(), name='add_subject'),
    path(route='gestion_ecole/matières/<int:pk>/editer/', view=EditSubjectView.as_view(), name='edit_subject'),
    path(route='gestion_ecole/matières/<int:pk>/delete/', view=SubjectView.as_view(), name='delete_subject'),
    
    
    path(route='gestion_ecole/programmes/', view=ProgramView.as_view(), name='programs'),
    path(route='gestion_ecole/programmes/ajouter/', view=AddProgramView.as_view(), name='add_program'),
    path(route='gestion_ecole/programmes/<int:pk>/editer/', view=EditProgramView.as_view(), name='edit_program'),
    path(route='gestion_ecole/programmes/<int:pk>/delete/', view=ProgramView.as_view(), name='delete_program'),
    
    path(route='gestion_ecole/sanctions-&-appreciations/', view=SanctionAppreciationView.as_view(), name='sanction_appreciations'),
    path(route='gestion_ecole/sanctions-&-appreciations/ajouter/', view=AddSanctionView.as_view(), name='add_sanction'),
    path(route='gestion_ecole/sanctions-&-appreciations/<int:pk>/editer/', view=EditSanctionView.as_view(), name='edit_sanction'),
    path(route='gestion_ecole/sanctions-&-appreciations/<int:pk>/delete/', view=SanctionAppreciationView.as_view(), name='delete_sanction'),
    
    path(route='gestion_ecole/trombinoscopes/', view=TrombinoscopeView.as_view(), name='trombinoscopes'),
    
    path(route='gestion_ecole/students/<int:pk>/detail/', view=StudentDetailView.as_view(), name='student_detail'),
    path(route='gestion_ecole/students/<int:pk>/edit/', view=EditStudentView.as_view(), name='edit_student'),
    path(route='gestion_ecole/students/ajouter/', view=AddStudentView.as_view(), name='add_student'),
    path(route='gestion_ecole/students/', view=StudentsView.as_view(), name='students'),
    path(route='gestion_ecole/students/<int:pk>/delete-document/', view=StudentDetailView.as_view(), name='student_delete_document'),
    
    path(route='gestion_ecole/teachers/', view=TeacherView.as_view(), name='teachers'),
    path(route='gestion_ecole/teachers/ajouter/', view=AddTeacherView.as_view(), name='add_teacher'),
    path(route='gestion_ecole/teachers/<int:pk>/editer/', view=EditTeacherView.as_view(), name='edit_teacher'),
    path(route='gestion_ecole/teachers/<int:pk>/delete/', view=TeacherView.as_view(), name='delete_teacher'),
    path(route='gestion_ecole/teachers/<int:pk>/detail/', view=TeacherDetailView.as_view(), name='teacher_detail'),
    path(route='gestion_ecole/teachers/<int:pk>/delete-document/', view=TeacherDetailView.as_view(), name='teacher_delete_document'),
    
    #===END
    
    #====================== THIS ROUTE IS FOR GESTION DU TEMPS MODULE =============================
    path(route='gestion_temps/emplois-du-temps/', view=ScheduleView.as_view(), name='times'),
    path(route='gestion_temps/emplois-du-temps/ajouter/', view=AddScheduleView.as_view(), name='add_time'),
    path(route='gestion_temps/emplois-du-temps/<int:pk>/delete/', view=ScheduleView.as_view(), name='delete_time'),
    
    #=================== THIS ROUTE IS FOR Communication MODULE ========================
    
    path(route='communication/informations/', view=InformationView.as_view(), name='informations'),
    path(route='communication/informations/<int:pk>/delete/', view=InformationView.as_view(), name='delete_information'),
    path(route='communication/informations/<int:pk>/detail/', view=InformationDetail.as_view(), name='info'),
    path(route='communication/informations/<int:pk>/edit/', view=EditInformationView.as_view(), name='edit_info'),
    path(route='communication/informations/ajouter/', view=AddInformationView.as_view(), name='add_information'),
    path(route='communication/events/', view=EventView.as_view(), name='events'),
    path(route='communication/events/<int:pk>/edit/', view=EditEventView.as_view(), name='edit_event'),
    path(route='communication/events/<int:pk>/delete/', view=EventView.as_view(), name='delete_events'),
    path(route='communication/events/<int:pk>/detail/', view=EventDetail.as_view(), name='event'),
    path(route='communication/events/ajouter/', view=AddEventView.as_view(), name='add_event'),
    #===ENDS
    
    #=========================== THIS ROUTE IS FOR CONTENUE PEDAGOGIQUE MODULE ======================#
    path(route='contenue_pedagogique/ebooks/', view=eBookView.as_view(), name="ebooks"),
    path(route='contenue_pedagogique/ebooks/ajouter/', view=AddeBook.as_view(), name='add_ebook'),
    path(route='contenue_pedagogique/ebooks/<int:pk>/delete/', view=eBookView.as_view(), name="delete_ebook"),
    path(route='contenue_pedagogique/ebooks/<int:pk>/edit/', view=EditEbook.as_view(), name="edit_ebook"),
    # path(route='contenue_pedagogique/dossiers/', view=FolderViews.as_view(), name='folders'),
    # path(route='contenue_pedagogique/dossiers/<int:folder_id>', view=FilesView.as_view(), name='content_folder'),
    # path(route='contenue_pedagogique/fichier/ajouter/', view=FilesView.as_view(), name='add_file'),
    #===END
    
    #============================ THIS ROUTE SI FOR BULLETIN & EVALUATIONS ==================================
    path(route='bulletins-&-évaluations/bulletins/<int:pk>/detail/', view=BulletinDetailView.as_view(), name='bulletin_detail'),
    path(route='bulletins-&-évaluations/bulletins/<int:pk>/detail/valided/', view=BulletinDetailView.check, name='bulletin_valid'),
    path(route='bulletins-&-évaluations/tableau-des-notes/', view=NoteTableView.as_view(), name='table_notes'),
    path(route='bulletins-&-évaluations/tableau-des-moyennes/', view=AverageTableView.as_view(), name='averages'),
    path(route='bulletins-&-évaluations/evaluations/', view=AssessmentView.as_view(), name='evaluations'),
    path(route='bulletins-&-évaluations/evaluations/ajouter/', view=AddAssessmentView.as_view(), name='add_evaluation'),
    path(route='bulletins-&-évaluations/evaluations/<int:pk>/edit/', view=EditAssessmentView.as_view(), name='edit_evaluation'),
    path(route='bulletins-&-évaluations/evaluations/<int:pk>/delete/', view=AssessmentView.as_view(), name='delete_evaluation'),
    #===END
    
    #=================== THIS ROUTE IS FOR Compte MODULE ===============================#
    path(route='comptes/compte_directions/', view=ListAllDirectionAccount.as_view(), name='directors'),
    path(route='comptes/compte_directions/ajouter/', view=AddDirectionAccount.as_view(), name='director_add'),
    path(route='comptes/compte_directions/<int:pk>/delete/', view=ListAllDirectionAccount.as_view(), name='director_delete'),
    path(route='comptes/compte_directions/<int:pk>/editer/', view=ListAllDirectionAccount.as_view(), name='director_edit'),
    
    path(route='comptes/compte_enseignants/', view=ListAllTeacherAccount.as_view(), name='teachers_account'),
    path(route='comptes/compte_enseignants/ajouter/', view=AddTeacherAccount.as_view(), name='add_teacher_account'),
    path(route='comptes/compte_enseignants/<int:pk>/delete/', view=ListAllTeacherAccount.as_view(), name='delete_teacher_account'),
    path(route='comptes/compte_enseignants/<int:pk>/edit/', view=EditTeacherAccountView.as_view(), name='edit_teacher_account'),
    
    path(route='comptes/compte_etudiants/', view=ListAllStudentAccount.as_view(), name='students_account'),
    path(route='comptes/compte_etudiants/ajouter/', view=AddStudentAccount.as_view(), name='add_student_account'),
    path(route='comptes/compte_etudiants/<int:pk>/delete/', view=ListAllStudentAccount.as_view(), name='delete_student_account'),
    path(route='comptes/compte_etudiants/<int:pk>/edit/', view=EditStudentAccountView.as_view(), name='edit_student_account'),
    #===END
    
    #=================== THIS ROUTE IS FOR ADMINISTRATION MODULE ========================
    path(route='administration/type_evaluation/', view=TypeEvaluationView.as_view(), name='type_evaluation'),
    path(route='administration/type_evaluation/<int:pk>/delete/', view=TypeEvaluationDeleteView.as_view(), name='delete_type_evaluation'),
    path(route='administration/type_documents/', view=TypeDocumentView.as_view(), name='type_documents'),
    path(route='administration/type_documents/<int:pk>/delete/', view=TypeDocumentDeleteView.as_view(), name='delete_type_document'),
    path(route='administration/type_documents/last/', view=get_last_document_type),
    path(route='administration/type_sanctions/', view=TypeSanctionView.as_view(), name='type_sanctions'),
    path(route='administration/type_sanctions/<int:pk>/delete/', view=TypeSanctionDeleteView.as_view(), name='delete_type_sanction'),
    path(route='administration/type_sanctions/last/', view=get_last_sanction_type),
    path(route='administration/reglage-general/', view=SettingAppView.as_view(), name='reglage_general'),
    path(route='administration/user-profile/', view=ProfileAppView.as_view(), name='user_profile'),
    path(route='administration/user-profile/edit/', view=EditProfileView.as_view(), name='edit_profil'),
    #===END
    
    #===================================== THIS ROUTE IS FOR STATISTIQUE MODULE ======================
    path(route='rapport-&-statistique/resultat-academique/', view=ResultatAcademique.as_view(), name='academic_result'),
    path(route='rapport-&-statistique/resultat-academique/close/', view=CloseAcademicYear.as_view(), name='close_year'),
    path(route="rapport-&-statistique/resultat-academique/bulletins/", view=ReportCardView.as_view(), name="bulletins"),
    path(route="rapport-&-statistique/resultat-academique/bulletins/ajouter/", view=AddReportCardView.as_view(), name="add_bulletin"),
    path(route="rapport-&-statistique/resultat-academique/bulletins/<int:pk>/editer/", view=EditReportCardView.as_view(), name="editer_bulletin"),
    path(route="rapport-&-statistique/resultat-academique/bulletins/<int:pk>/delete/", view=ReportCardView.as_view(), name="delete_bulletin"),
    path(route='rapport-&-statistique/monter-en-niveau/', view=NextLevelView.as_view(), name='next_level'),
    path(route='rapport-&-statistique/monter-en-niveau/<int:pk>/unChecked/', view=NextLevelView.unChecked, name='past_level'),
    path(route='rapport-&-statistique/monter-en-niveau/<int:pk>/ajouter/', view=AddNextLevelView.as_view(), name='add_next_level'),
    
    path(route='no-academic-year-found/', view=NotAcademicYearFound.as_view(), name='no_year'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)