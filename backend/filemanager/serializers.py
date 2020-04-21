from rest_framework import serializers
from .models import Exercice


class ExerciceSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    # pk = serializers.SerializerMethodField()
    # size = serializers.SerializerMethodField()
    # name = serializers.SerializerMethodField()
    filetype = serializers.SerializerMethodField()
    # since_added = serializers.SerializerMethodField()

    class Meta:
        model = Exercice
        fields = '__all__'

    # def get_pk(self, obj):
    #     return obj.pk
    #
    # def get_size(self, obj):
    #     file_size = ''
    #     if obj.file and hasattr(obj.file, 'size'):
    #         file_size = obj.file.size
    #     return file_size
    #
    # def get_name(self, obj):
    #     file_name = ''
    #     if obj.file and hasattr(obj.file, 'name'):
    #         return obj.file.name.split('.')[0]
    #     return file_name
    #
    def get_filetype(self, obj):
        if obj.file:
            filename = obj.file.name
            return filename.split('.')[-1]
        return None
    #
    # def get_since_added(self, obj):
    #     date_added = obj.date_created
    #     return date_added

