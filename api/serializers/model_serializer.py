from rest_framework import serializers
from backend.models.communication import Information, Event
from backend.models.contenue_pedagogique import eBook
from backend.models.evaluations import Assessment
from backend.models.facturation import FinancialCommitment, Invoice
from backend.models.gestion_ecole import Schedule
from backend.models.user_account import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
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

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'


class FinancialCommitmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialCommitment
        fields = '__all__'

