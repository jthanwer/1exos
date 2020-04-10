from rest_framework import serializers
from .models import Exercice


class ExerciceSerializer(serializers.ModelSerializer):
    size = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    filetype = serializers.SerializerMethodField()
    since_added = serializers.SerializerMethodField()

    class Meta:
        model = Exercice
        fields = ('file_id', 'file', 'size', 'name', 'filetype', 'since_added')

    def get_size(self, obj):
        file_size = ''
        if obj.file and hasattr(obj.file, 'size'):
            file_size = obj.file.size
        return file_size

    def get_name(self, obj):
        file_name = ''
        if obj.file and hasattr(obj.file, 'name'):
            file_name = obj.file.name
        return file_name

    def get_filetype(self, obj):
        filename = obj.file.name
        return filename.split('.')[-1]

    def get_since_added(self, obj):
        date_added = obj.date_created
        return date_added

