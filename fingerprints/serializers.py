from rest_framework import serializers
from .models import Worker, FingerprintImage

class FingerprintImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FingerprintImage
        fields = ['id', 'worker', 'image', 'uploaded_at']

class WorkerSerializer(serializers.ModelSerializer):
    fingerprints = FingerprintImageSerializer(many=True, read_only=True)

    class Meta:
        model = Worker
        fields = ['id', 'name', 'fingerprints']