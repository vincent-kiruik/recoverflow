from rest_framework import serializers
from .models import Collection

class CollectionSerializer(serializers.ModelSerializer):
    collected_by_name = serializers.CharField(source='collected_by.full_name', read_only=True)

    class Meta:
        model = Collection
        fields = [
            'id', 'recovery_case', 'loan', 'amount_collected', 'payment_method',
            'receipt_number', 'collected_by', 'collected_by_name', 'verified_by',
            'collection_date', 'notes'
        ]