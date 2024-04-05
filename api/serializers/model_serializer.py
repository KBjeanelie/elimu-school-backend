from rest_framework import serializers
from backend.models.communication import Information, Event
from backend.models.contenue_pedagogique import eBook
from backend.models.evaluations import Assessment
from backend.models.facturation import FinancialCommitment, Invoice, Item
from backend.models.gestion_ecole import ClassRoom, GroupSubject, Schedule, Student, Subject, AcademicYear, Teacher
from backend.models.user_account import User

class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

class GroupSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupSubject
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    teacher_in_charge = TeacherSerializer()
    subject_group = GroupSubjectSerializer()
    class Meta:
        model = Subject
        fields = '__all__'

class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = '__all__'
        
class eBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = eBook
        fields = '__all__'

class InformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Information
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class AssessmentSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()
    classroom = ClassroomSerializer()
    class Meta:
        model = Assessment
        fields = '__all__'


class InvoiceSerializer(serializers.ModelSerializer):
    item = ItemSerializer()
    classroom = ClassroomSerializer()
    academic_year = AcademicYearSerializer()
    class Meta:
        model = Invoice
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'


class FinancialCommitmentSerializer(serializers.ModelSerializer):
    academic_year = AcademicYearSerializer()
    class Meta:
        model = FinancialCommitment
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

