from rest_framework import serializers
from .models import FollowUpAction

class FollowUpActionSerializer(serializers.ModelSerializer):
    officer_name = serializers.CharField(source='officer.full_name', read_only=True)

    class Meta:
        model = FollowUpAction
        fields = [
            'id', 'recovery_case', 'officer', 'officer_name', 'action_type',
            'notes', 'result', 'promise_amount', 'promise_date', 'next_action_date',
            'gps_latitude', 'gps_longitude', 'attachment', 'created_at'
        ]