from rest_framework import serializers
from .models import Exercice, Correction, Rating
from users.serializers import BasicUserSerializer
import decimal
from django.db.models import Avg



class PreviewCorrectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Correction
        fields = ('id', 'prix')


class ExerciceSerializer(serializers.ModelSerializer):
    posteur = BasicUserSerializer(read_only=True)
    niveau = serializers.IntegerField(read_only=True)
    prefix_prof = serializers.BooleanField(read_only=True)
    nom_prof = serializers.CharField(read_only=True)
    ville_etablissement = serializers.CharField(read_only=True)
    nom_etablissement = serializers.CharField(read_only=True)
    correcs = PreviewCorrectionSerializer(many=True, read_only=True)
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


class LightCorrectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Correction
        fields = ('id', 'correcteur')


class CorrectionSerializer(serializers.ModelSerializer):
    correcteur = serializers.StringRelatedField(read_only=True)
    enonce = ExerciceSerializer(read_only=True)
    enonce_id = serializers.IntegerField(write_only=True)
    name = serializers.SerializerMethodField()
    mean_rating = serializers.SerializerMethodField()
    filetype = serializers.SerializerMethodField()

    class Meta:
        model = Correction
        fields = '__all__'

    def get_mean_rating(self, obj):
        if obj.ratings.exists():
            mean_value = obj.ratings.aggregate(Avg('value'))['value__avg']
            return mean_value
        return None

    def get_name(self, obj):
        if obj.file and hasattr(obj.file, 'name'):
            return obj.file.name
        return None

    def get_filetype(self, obj):
        if obj.file:
            filename = obj.file.name
            return filename.split('.')[-1]
        return None


class RatingSerializer(serializers.ModelSerializer):
    voter = serializers.StringRelatedField(read_only=True)
    correc_id = serializers.IntegerField(write_only=True)
    correc = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Rating
        fields = '__all__'
