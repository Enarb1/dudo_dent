from datetime import datetime

from django.contrib.auth import get_user_model
from rest_framework import serializers

from Dudo_dent.appointments.models import Appointment


UserModel = get_user_model()

class AppointmentSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='patient.full_name', read_only=True)
    start = serializers.SerializerMethodField()
    end = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    dentist_id = serializers.IntegerField(source='dentist.id', read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Appointment
        fields = ('id', 'title', 'start', 'end', 'dentist_id', 'url')

    def get_start(self, obj):
        return datetime.combine(obj.date, obj.start_time).isoformat()

    def get_end(self, obj):
        return datetime.combine(obj.date, obj.end_time).isoformat()

    def get_url(self, obj):
        return obj.get_absolute_url()

