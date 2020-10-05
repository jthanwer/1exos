from rest_framework import serializers
from .models import Exercice, Correction, Rating
from notifications.models import Notification
from users.serializers import BasicUserSerializer
from django.db.models import Avg

import decimal

class PreviewCorrectionSerializer(serializers.ModelSerializer):
    mean_rating = serializers.SerializerMethodField()
    before_deadline = serializers.SerializerMethodField()

    class Meta:
        model = Correction
        fields = ('id', 'correcteur', 'prix', 'mean_rating', 'before_deadline')

    def get_mean_rating(self, obj):
        if obj.ratings.exists():
            mean_value = obj.ratings.aggregate(Avg('value'))['value__avg']
            return mean_value
        return None

    def get_before_deadline(self, obj):
        before_deadline = obj.date_created <= obj.enonce.date_limite
        return before_deadline


class PreviewEnonceSerializer(serializers.ModelSerializer):
    posteur = BasicUserSerializer(read_only=True)

    class Meta:
        model = Exercice
        fields = ('id', 'niveau', 'type',
                  'livre', 'num_page', 'num_exo',
                  'posteur', 'prix')


class ExerciceSerializer(serializers.ModelSerializer):
    posteur = BasicUserSerializer(read_only=True)
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
        if obj.file:
            if hasattr(obj.file, 'name'):
                return obj.file.name
        return None

    def get_filetype(self, obj):
        if obj.file:
            filename = obj.file.name
            return filename.split('.')[-1]
        return None


class CorrectionSerializer(serializers.ModelSerializer):
    correcteur = serializers.StringRelatedField(read_only=True)
    enonce = PreviewEnonceSerializer(read_only=True)
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


# ----------------------------
# -- Notification serializer
# ----------------------------

class GenericNotificationRelatedField(serializers.RelatedField):

    def to_representation(self, value):
        if isinstance(value, Correction):
            serializer = PreviewCorrectionSerializer(value)
        if isinstance(value, Exercice):
            serializer = PreviewEnonceSerializer(value)

        return serializer.data


class NotificationSerializer(serializers.ModelSerializer):
    recipient = BasicUserSerializer()
    target = GenericNotificationRelatedField(read_only=True)
    action_object = GenericNotificationRelatedField(read_only=True)

    class Meta:
        model = Notification
        fields = ('id', 'unread', 'recipient',
                  'verb', 'target', 'action_object',
                  'timestamp')
