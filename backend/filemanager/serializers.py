from rest_framework import serializers
from .models import Exercice, Correction
from users.serializers import BasicUserSerializer
import decimal


class PreviewCorrectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Correction
        fields = ('id', 'prix')


class ExerciceSerializer(serializers.ModelSerializer):
    posteur = BasicUserSerializer(read_only=True)
    # size = serializers.SerializerMethodField()
    corrections = PreviewCorrectionSerializer(many=True, read_only=True)
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
    correcteur = serializers.StringRelatedField(read_only=True)
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
    prix = serializers.IntegerField()

    def validate_prix(self, value):
        return value
