from rest_framework import serializers
from .models import Exercice, Correction
import decimal


class ExerciceSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    # size = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    filetype = serializers.SerializerMethodField()

    class Meta:
        model = Exercice
        fields = '__all__'

    def get_name(self, obj):
        if obj.file and hasattr(obj.file, 'name'):
            return obj.file.name
        return None

    def get_filetype(self, obj):
        if obj.file:
            filename = obj.file.name
            return filename.split('.')[-1]
        return None


class CorrectionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    enonce = ExerciceSerializer(read_only=True)
    enonce_id = serializers.IntegerField(write_only=True)
    name = serializers.SerializerMethodField()
    filetype = serializers.SerializerMethodField()

    class Meta:
        model = Correction
        fields = '__all__'

    def get_name(self, obj):
        if obj.file and hasattr(obj.file, 'name'):
            return obj.file.name
        return None

    def get_filetype(self, obj):
        if obj.file:
            filename = obj.file.name
            return filename.split('.')[-1]
        return None


class UnlockCorrectionSerializer(serializers.Serializer):
    price = serializers.DecimalField(max_digits=5, decimal_places=2)

    def validate_price(self, value):
        return value
